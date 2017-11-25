import aiohttp
import uvloop
import asyncio
import re
import sys
import logging
# import reporting
from lxml import etree
import time
from urllib.parse import urlparse, splitport, urljoin
from contextlib import closing
from collections import namedtuple

try:
    # Python 3.4.
    from asyncio import JoinableQueue as Queue
except ImportError:
    # Python 3.5.
    from asyncio import Queue

logging.basicConfig(filename='zcn.log', level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

"""2017-11-24 11:17:59
"""

"""lenient mode
www.amazcon.com => amazcon.com
"""

FetchStatistic = namedtuple('FetchStatistic',['url'])


def lenient_host(host):
    parts = host.split('.')[-2:]
    return '.'.join(parts)


def is_redirect(response):
    print(response.status)
    return response.status in (300, 301, 302, 303, 307)

class Crawl:
    def __init__(self, roots, strict=True, max_redirect=10, max_tries=4, max_tasks=10, *, loop=None):
        self.t0 = time.time()
        self.t1 = None
        self.strict = strict
        self.max_redirect = max_redirect
        self.max_tries = max_tries
        self.max_tasks = max_tasks
        self.loop = loop or asyncio.get_event_loop()
        self.q = Queue(loop=self.loop)
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.root_domains = set()
        self.seen_urls = set()
        self.done = []
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
        links = set()
        # print(await response.read())
        text = await response.text()
        # print(text)
        urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''',
                              text))
        # print(response.url)
        for url in urls:
            links.add(url)
        print(urls)
        stat = FetchStatistic(url=response.url)
        print(stat)
        return stat, links

    async def fetch(self, url, max_redirect):
        tries = 0
        exception = None
        while tries < self.max_tries:
            try:
                print("fetch function is doing...")
                response = await self.session.get(url, allow_redirects=False)
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
                LOGGER.info('2222222')
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
    # loop = uvloop.new_event_loop()
    # asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    zcn_root = "https://www.amazon.cn/s/ref=lp_658390051_nr_n_28?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658401051&bbn=658391051&ie=UTF8&qid=1511335822&rnid=658391051"
    demo_url = "http://127.0.0.1"
    baidu_url = "http://www.baidu.com"
    roots = [
        demo_url
        # baidu_url
        # zcn_root,
        # demo_root,
        # zcn_root2
    ]

    crawler = Crawl(roots)
    try:
        loop.run_until_complete(crawler.crawl())  # Crawler gonna crawl.
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
        # https://www.amazon.cn/s/ref=lp_658390051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051&bbn=658391051&ie=UTF8&qid=1511403641&rnid=658391051
        # https://www.amazon.cn/s/ref=lp_658394051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051&bbn=658394051&ie=UTF8&qid=1511506580&rnid=658394051
        # https://www.amazon.cn/s/ref=lp_658508051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051%2Cn%3A659356051&bbn=658508051&ie=UTF8&qid=1511506663&rnid=658508051
        # https://www.amazon.cn/s/ref=lp_658508051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051%2Cn%3A659356051&bbn=658508051&ie=UTF8&qid=1511506663&rnid=658508051
        # https://www.amazon.cn/s/ref=lp_658508051_nr_n_1?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051%2Cn%3A659357051&bbn=658508051&ie=UTF8&qid=1511506663&rnid=658508051