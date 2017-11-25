from config import headers

import aiohttp
import asyncio
import time

from lxml import etree

async def fetch(session, url):
    with aiohttp.Timeout(100):
        async with session.get(url) as response:
            text = await response.text()
            tree = etree.HTML(text)
            
            links= []
            elements = tree.xpath('//*[@data-typeid="n"]/li[@style="margin-left: 6px"]/a')
            for e in elements:
                # r = await asyncio.gather(
                #     *[fetch(session, "https://www.amazon.cn"+e.get('href'))],
                #     return_exceptions=True  # default is false, that would raise
                # )
                links.append("https://www.amazon.cn"+e.get('href'))
            print(links)
            results = await asyncio.gather(
                *[fetch_one(session, url) for url in links],
                return_exceptions=True  # default is false, that would raise
            )
            return results
            # return r
                # print("https://www.amazon.cn"+e.get('href'))
                # return await fetch_one(session, "https://www.amazon.cn"+e.get('href'))
                # links.append( {"href": e.get('href'), 'title': e.find('span').text} )
            # return links
            # """
            # ref = tree.xpath('string(//*[@data-typeid="n"]/@id)')
            # ref_id = ref.split('_')[1]
            # print("first page id is {}".format(ref_id))
            # return ref_id
            
async def fetch_one(session, url):
    with aiohttp.Timeout(100):
        async with session.get(url) as response:
            print(url)
            text = await response.text()
            tree = etree.HTML(text)
            """
            links= []
            elements = tree.xpath('//*[@data-typeid="n"]/li[@style="margin-left: -2px"]/a')
            for e in elements:
                links.append( {"href": e.get('href'), 'title': e.find('span').text} )
            return links
            """
            ref = tree.xpath('string(//*[@data-typeid="n"]/@id)')
            ref_id = ref.split('_')[1]
            return ref_id
            

# async def fetch_all(session, urls, loop):
#     results = await asyncio.gather([loop.create_task(fetch(session, url))
#                                   for url in urls])
#     return results

async def fetch_all(session, urls, loop):
    results = await asyncio.gather(
        *[fetch(session, url) for url in urls],
        return_exceptions=True  # default is false, that would raise
    )

    # for testing purposes only
    # gather returns results in the order of coros
    for idx, url in enumerate(urls):
        print('{}: {}'.format(url, 'ERR' if isinstance(results[idx], Exception) else 'OK'))
    return results


if __name__ == '__main__':
    # baseurl = "https://www.amazon.cn/s/ref=lp_658415051_ex_n_1?rh=n%3A658390051&bbn=658390051&ie=UTF8&qid=1511332205"
    baseurl = "https://www.amazon.cn/s/ref=lp_658390051_nr_n_28?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658401051&bbn=658391051&ie=UTF8&qid=1511335822&rnid=658391051"
    start = time.time()
    # 添加uvloop
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    # 本来是批量的,现在有个种子文件.
    # urls = [ baseurl,baseurl ]
    urls = [baseurl]
    with aiohttp.ClientSession(loop=loop) as session:
        htmls = loop.run_until_complete(
            fetch_all(session, urls, loop))
        print(htmls)
        
    print("执行时间为: {}".format(time.time()-start))


"""

ll = []
req = requests.get(url)
tree = etree.HTML(req.text)
links = tree.xpath('//*[@data-typeid="n"]/li[@style="margin-left: 6px"]/a')
# print(links)
for i in links:
    ll.append({'a': i.get('href'), 'b': i.find('span').text})
print(ll)

"""

# baseurl = "https://www.amazon.cn/s/ref=lp_658415051_ex_n_1?rh=n%3A658390051&bbn=658390051&ie=UTF8&qid=1511332205"
