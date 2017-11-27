import aiohttp
import uvloop
import asyncio
import re
import sys
import logging
# import reporting
# from lxml import etree
import time
from urllib.parse import urlparse, splitport, urljoin,urldefrag
from contextlib import closing
from collections import namedtuple
import random
import cgi
import math
import os
from configparser import ConfigParser
# import urllib.parse
try:
    # Python 3.4.
    from asyncio import JoinableQueue as Queue
except ImportError:
    # Python 3.5.
    from asyncio import Queue

# logging.basicConfig(filename='zcn3.log', level=logging.DEBUG, handlers={})
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
handler = logging.FileHandler('zcn.log', 'a', 'utf-8')
LOGGER.addHandler(handler)


#TODO 错误尝试数优化.

"""2017-11-24 11:17:59
"""

"""lenient mode
www.amazcon.com => amazcon.com
"""

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )


FetchStatistic = namedtuple('FetchStatistic',['url'])
PriceLowHigh = namedtuple('PriceLowHigh',['low','high'])


def lenient_host(host):
    parts = host.split('.')[-2:]
    return '.'.join(parts)


def is_redirect(response):
    # print(response.status)
    return response.status in (300, 301, 302, 303, 307)

class Crawl:
    def __init__(self, roots, exclude=None,
                 strict=True,
                 base_url = None,
                 max_redirect=2, max_tries=2, max_tasks=1, proxy=None, *, loop=None):
        self.base_url = base_url
        self.t0 = time.time()
        self.t1 = None
        self.strict = strict
        self.exclude = exclude
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.loop = loop or asyncio.get_event_loop()
        self.q = Queue(loop=self.loop)
        self.proxy = proxy
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.root_domains = set()
        self.seen_urls = set()
        self.done = []
        # self.headers=
        for root in roots:
            parts = urlparse(root)
            host, port = splitport(parts.netloc)
            if not host:
                continue
            if re.match(r'\A[\d\.]*\Z', host):
                self.root_domains.add(host)
            else:
                host = host.lower()
                if self.strict:
                    self.root_domains.add(host)
                else:
                    self.root_domains.add(lenient_host(host))
        for root in roots:
            self.add_url(root)

    def add_url(self, url, max_redirect=None):
        if max_redirect is None:
            max_redirect = self.max_redirect
        self.seen_urls.add(url)
        self.q.put_nowait( (url, max_redirect))

    def record_statistic(self, fetch_statistic):
        """Record the FetchStatistic for completed / failed URL."""
        self.done.append(fetch_statistic)

    async def parse_links(self, response):
        print('解析网页')
        links = set()
        content_type = None
        encoding = None
        # print(await response.read())
        if response.status == 200:
            content_type = response.headers.get('content-type')
            print(content_type)
            if content_type in ('text/html', 'application/xml', 'text/html;charset=UTF-8'):
                pdict = {}
                if content_type:
                    content_type, pdict = cgi.parse_header(content_type)

                encoding = pdict.get('charset', 'utf-8')
                if content_type in ('text/html', 'application/xml'):
                    text = await response.text()
                    # print(text)
                    '''(?i)href=["']([^\s"'<>]+)'''
                    urls = set(re.findall('<li style="margin-left: [-\d]+px">.*?<a href="(/s/ref=lp_\d+_nr_n_[\d+].*?)">.*?<span class="refinementLink">(.*?)</span>.*?</a>.*?</li>',
                                          text, re.S|re.M))
                    print(urls)
                    # if not len(urls):
                    #     print('空的.应该是最后的连接了')
                    #     prices = [(low, low+1) for low in range(1,100,2)]
                    #     for price in prices:
                    #         low, height = price
                    #         LOGGER.info("细分分类价格链接: %s&low-price=%s&high-price=%s", str(response.url), low, height)

                    if urls:
                        LOGGER.info('got %r distinct urls from %r', len(urls), response.url)
                    else:
                        prices = [(price_g, price_g+1) for price_g in range(1,100,2)]
                        try:
                            for price in prices:
                                p = PriceLowHigh._make(price)
                                LOGGER.debug("细分分类价格链接: %s&low-price=%s&high-price=%s ", str(response.url), p.low, p.high)
                        except Exception as e:
                            print(e)
                    # print(len(urls))
                    for url in urls:
                        u, t = url
                        k = u.replace('&amp;', '&')
                        normalized = urljoin(str(response.url), k)
                        defragmented, frag = urldefrag(normalized)
                        print(defragmented)
                        print('我已经进入下一级')
                        if self.url_allowed(defragmented):
                            print(defragmented,t)
                            ''' Children's Books（儿童图书） General (科学通俗读物) 这两个陷入了回调.
                            INFO:__main__:redirect to 'https://www.amazon.cn/s/ref=lp_2084813051_nr_n_11/460-8646033-3118437?rh=n%3A2084813051&ie=UTF8' from 
'https://www.amazon.cn/s/ref=lp_2084813051_nr_n_11/460-8646033-3118437?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A2045366051%2Cn%3A2078652051%2Cn%3A2084813051%2Cn%3A2084839051&bbn=2084813051&ie=UTF8&qid=1511710241&rnid=2084813051'
'''
                            LOGGER.info = LOGGER.debug('previous url: %s, next url: %s, title: %s',str(response.url), defragmented, t)
                            # LOGGER.info("中国".encode('utf-8').decode('utf-8'))
                            # logging.warning("helo")
                            if t == "General (科学通俗读物)":
                                # pass
                                LOGGER.error("错误的分类: %r", t)
                            else:
                                print('add links....')
                                links.add(defragmented)

        stat = FetchStatistic(url=response.url)
        return stat, links

    async def fetch(self, url, max_redirect):
        tries = 0
        exception = None
        while tries < self.max_tries:
            try:
                # print("fetch function is doing...")
                headers = {
                    'User-Agent': FakeChromeUA.get_ua(),
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Connection': 'keep-alive'
                }
                response = await self.session.get(url, allow_redirects=False, headers=headers) #proxy=self.p,
                if tries > 1:
                    LOGGER.info = LOGGER.info('try %r for %r success', tries, url)
                break
            except aiohttp.ClientError as client_error:
                LOGGER.info('try %r for %r raised %r', tries, url, client_error)
                exception = client_error
            tries += 1
        else:
            LOGGER.error('%r failed after %r tries',
                         url, self.max_tries)
            return

        try:
            if is_redirect(response):
                location = response.headers['location']
                next_url = urljoin(url, location)
                if next_url in self.seen_urls:
                    return
                if max_redirect > 0:
                    LOGGER.info('redirect to %r from %r', next_url, url)
                    self.add_url(next_url, max_redirect - 1)
                else:
                    LOGGER.error('redirect limit reached for %r from %r',
                                 next_url, url)
            else:
                # LOGGER.info('ubuntu ing')
                stat, links = await self.parse_links(response)
                self.record_statistic(stat)
                for link in links.difference(self.seen_urls):
                    self.q.put_nowait((link, self.max_redirect))
                self.seen_urls.update(links)
        finally:
            await response.release()

    async def work(self):
        try:
            while True:
                url, max_redirect = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url, max_redirect)
                self.q.task_done()
        except asyncio.CancelledError:
            pass

    def host_okay(self, host):
        """Check if a host should be crawled.

        A literal match (after lowercasing) is always good.  For hosts
        that don't look like IP addresses, some approximate matches
        are okay depending on the strict flag.
        """
        host = host.lower()
        if host in self.root_domains:
            return True
        if re.match(r'\A[\d\.]*\Z', host):
            return False
        if self.strict:
            return self._host_okay_strictish(host)
        else:
            return self._host_okay_lenient(host)

    def _host_okay_strictish(self, host):
        """Check if a host should be crawled, strict-ish version.

        This checks for equality modulo an initial 'www.' component.
        """
        host = host[4:] if host.startswith('www.') else 'www.' + host
        return host in self.root_domains

    def _host_okay_lenient(self, host):
        """Check if a host should be crawled, lenient version.

        This compares the last two components of the host.
        """
        return lenient_host(host) in self.root_domains

    def url_allowed(self, url):
        if self.exclude and re.search(self.exclude, url):
            return False
        parts = urlparse(url)
        if parts.scheme not in ('http', 'https'):
            LOGGER.debug('skipping non-http scheme in %r', url)
            return False
        host, port = splitport(parts.netloc)
        if not self.host_okay(host):
            LOGGER.debug('skipping non-root host in %r', url)
            return False
        return True

    async def crawl(self):
        """Run the crawler until all finished."""
        workers = [asyncio.Task(self.work(), loop=self.loop)
                 for _ in range(self.max_tasks)]
        self.t0 = time.time()
        await self.q.join()
        self.t1 = time.time()
        for w in workers:
            w.cancel()

    def close(self):
        self.session.close()

    def check_result(self):
        print(self.root_domains)

    def __call__(self):
        print("__call__ function")
        print(self.root_domains)


if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    roots = [
        # 'https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=sa_menu_top_books_l1?ie=UTF8&node=658390051'
        # 'https://www.amazon.cn/s/ref=lp_658508051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051%2Cn%3A659356051&bbn=658508051&ie=UTF8&qid=1511762114&rnid=658508051'
        'https://www.amazon.cn/s/ref=lp_658390051_nr_n_6?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658683051&bbn=658391051&ie=UTF8&qid=1511768359&rnid=658391051'
    ]

    cfg = ConfigParser()
    cfg.read(os.path.expanduser('~/.config_crawl.ini'))
    base_url = cfg.get('zcn', 'base_url')
    is_proxy = False
    if is_proxy:
        proxy = cfg.get('proxy', 'auth_proxy')
        crawler = Crawl(roots, proxy=proxy)
    else:
        proxy = None
        crawler = Crawl(roots, base_url= base_url)

    try:
        a1 = time.time()
        loop.run_until_complete(crawler.crawl())  # Crawler gonna crawl.
        print('cost time: {}'.format(time.time()-a1))
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('\nInterrupted\n')
    finally:
        # reporting.report(crawler)
        crawler.close()

        # next two lines are required for actual aiohttp resource cleanup
        loop.stop()
        loop.run_forever()

        loop.close()
