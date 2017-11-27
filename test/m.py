import asyncio
import cgi
from collections import namedtuple
import logging
import re
import time
import urllib.parse
import uvloop

try:
    # Python 3.4.
    from asyncio import JoinableQueue as Queue
except ImportError:
    # Python 3.5.
    from asyncio import Queue

import aiohttp  # Install with "pip install aiohttp".

logging.basicConfig(filename='example.log', level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

xpathCollect = namedtuple('xpathCollect', ['xpath1', 'xpath2', 'xpath3'])
xpathCollect(
    xpath1='//*[@data-typeid="n"]/li[@style="margin-left: -2px"]/a',
    xpath2='//*[@data-typeid="n"]/li[@style="margin-left: -2px"]/a',
    xpath3='//*[@data-typeid="n"]/li[@style="margin-left: -2px"]/a')

def is_redirect(response):
    return response.status in (300, 301, 302, 303, 307)

FetchStatistic = namedtuple('FetchStatistic', ['url',
                                               'next_url',
                                               'status',
                                               'exception',
                                               'size',
                                               'content_type',
                                               'encoding',
                                               'num_urls',
                                               'num_new_urls'])


class Crawler:
    """construct crawler
    root: baseurl
    max_tasks
    max_tries
    """

    def __init__(self, roots, exclude=None, max_tasks=10, max_redirect=10, max_tries=5, *, loop=None):
        self.roots = roots
        self.exclude = exclude
        self.loop = loop or asyncio.get_event_loop()
        self.q = Queue(loop=self.loop)
        self.max_tasks = max_tasks
        self.max_tries = max_tries
        self.max_redirect = max_redirect
        self.done = []
        self.seen_urls = set()
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.root_domains = set()
        for root in roots:
            self.add_url(root)
        self.t0 = time.time()
        self.t1 = None

    def url_allowed(self, url):
        if self.exclude and re.search(self.exclude, url):
            return False
        parts = urllib.parse.urlparse(url)
        if parts.scheme not in ('http', 'https'):
            LOGGER.debug('skipping non-http scheme in %r', url)
            return False
        host, port = urllib.parse.splitport(parts.netloc)
        if not self.host_okay(host):
            LOGGER.debug('skipping non-root host in %r', url)
            return False
        return True

    def add_url(self, url, max_redirect=None):
        # print("hello world")
        if max_redirect is None:
            max_redirect = self.max_redirect
        logging.info('adding %r %r', url, max_redirect)
        self.seen_urls.add(url)
        self.q.put_nowait((url, max_redirect))

    def record_statistic(self, fetch_statistic):
        """Record the FetchStatistic for completed / failed URL."""
        self.done.append(fetch_statistic)

    async def parse_links(self, response):
        """Return a FetchStatistic and list of links."""
        links = set()
        content_type = None
        encoding = None
        body = await response.read()

        if response.status == 200:
            content_type = response.headers.get('content-type')
            pdict = {}

            if content_type:
                content_type, pdict = cgi.parse_header(content_type)

            encoding = pdict.get('charset', 'utf-8')
            if content_type in ('text/html', 'application/xml'):
                text = await response.text()

                # Replace href with (?:href|src) to follow image links.
                urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''',
                                      text))
                if urls:
                    LOGGER.info('got %r distinct urls from %r',
                                len(urls), response.url)
                for url in urls:
                    normalized = urllib.parse.urljoin(response.url, url)
                    defragmented, frag = urllib.parse.urldefrag(normalized)
                    if self.url_allowed(defragmented):
                        links.add(defragmented)

        stat = FetchStatistic(
            url=response.url,
            next_url=None,
            status=response.status,
            exception=None,
            size=len(body),
            content_type=content_type,
            encoding=encoding,
            num_urls=len(links),
            num_new_urls=len(links - self.seen_urls))

        return stat, links

    async def fetch(self, url, max_redirect):
        """Fetch one URL."""
        tries = 0
        exception = None
        while tries < self.max_tries:
            try:
                response = await self.session.get(
                    url, allow_redirects=False)

                if tries > 1:
                    LOGGER.info('try %r for %r success', tries, url)

                break
            except aiohttp.ClientError as client_error:
                LOGGER.info('try %r for %r raised %r', tries, url, client_error)
                exception = client_error

            tries += 1
        else:
            # We never broke out of the loop: all tries failed.
            LOGGER.error('%r failed after %r tries',
                         url, self.max_tries)
            self.record_statistic(FetchStatistic(url=url,
                                                 next_url=None,
                                                 status=None,
                                                 exception=exception,
                                                 size=0,
                                                 content_type=None,
                                                 encoding=None,
                                                 num_urls=0,
                                                 num_new_urls=0))
            return

        try:
            if is_redirect(response):
                location = response.headers['location']
                next_url = urllib.parse.urljoin(url, location)
                self.record_statistic(FetchStatistic(url=url,
                                                     next_url=next_url,
                                                     status=response.status,
                                                     exception=None,
                                                     size=0,
                                                     content_type=None,
                                                     encoding=None,
                                                     num_urls=0,
                                                     num_new_urls=0))

                if next_url in self.seen_urls:
                    return
                if max_redirect > 0:
                    LOGGER.info('redirect to %r from %r', next_url, url)
                    self.add_url(next_url, max_redirect - 1)
                else:
                    LOGGER.error('redirect limit reached for %r from %r',
                                 next_url, url)
            else:
                stat, links = await self.parse_links(response)
                self.record_statistic(stat)
                for link in links.difference(self.seen_urls):
                    self.q.put_nowait((link, self.max_redirect))
                self.seen_urls.update(links)
        finally:
            await response.release()

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

    async def work(self):
        try:
            while True:
                url, max_redirect = await self.q.get()
                assert url in self.seen_urls
                await self.fetch(url, max_redirect)
                self.q.task_done()
        except asyncio.CancelledError:
            pass

    def __repr__(self):
        return "hello Crawler class"


if __name__ == '__main__':
    """use uvloop.it's best loop for"""
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)

    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too, hello world')

    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    roots = ['http://127.0.0.1/1.htm']
    c = Crawler(roots=roots)
    c.work()
    c.close()

    # pass
    # print(__name__)
    # print(Crawler())
