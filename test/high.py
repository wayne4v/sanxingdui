"""aiohttp-based client to retrieve web pages.
"""

import asyncio
from contextlib import closing
import time

import aiohttp


async def fetch_page(session, host, port=8000, wait=0):
    """Get one page.
    """
    # await asyncio.sleep(wait)
    url = host#= '{}:{}/{}'.format(host, port, wait)
    with aiohttp.Timeout(10):
        await asyncio.sleep(wait)
        async with session.get(url) as response:
            assert response.status == 200
            print(response.status)
            return await response.text()

            # return await str(response.status)

def get_multiple_pages(host, waits, port=8000, show_time=True):
    """Get multiple pages.
    """
    tasks = []
    pages = []
    start = time.perf_counter()
    with closing(asyncio.get_event_loop()) as loop:
        with aiohttp.ClientSession(loop=loop) as session:
            for wait in waits:
                tasks.append(fetch_page(session, host, port, wait))
            pages = loop.run_until_complete(asyncio.gather(*tasks))
    duration = time.perf_counter() - start
    sum_waits = sum(waits)
    if show_time:
        msg = 'It took {:4.2f} seconds for a total waiting time of {:4.2f}.'
        print(msg.format(duration, sum_waits))
    return pages


if __name__ == '__main__':

    def main():
        """Test it.
        """
        pages = get_multiple_pages(host='http://httpbin.org/ip', port=80,
                                   waits=[2,4,6])
        for page in pages:
            print(page)

    main()
