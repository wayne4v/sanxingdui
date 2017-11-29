import requests
import html
import re
from urllib.parse import urlparse
import math

header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"}

def parse_page_book(url, header):
    rep = requests.get(url, headers=header)
    text = rep.text
    pattern = '''<a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal" target="_blank" title="(.*?)" href="(.*?)">.*?</a>'''
    books = re.findall(pattern, text)
    # print(books)
    for info in books:
        title, link = info
        print("title:{}, link:{}".format(html.unescape(title), link))

price_link = "https://www.amazon.cn/s/ref=sr_nr_p_36_0?rnid=664971051&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658393051%2Cn%3A658495051%2Cp_36%3A100-2000&qid=1511960661&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&bbn=658495051&low-price=1&high-price=10&x=0&y=0"
o = urlparse(price_link)
query = o.query
# print(o.query)

req = requests.get(price_link, headers=header)
text = req.text
book_count_parse = re.findall("显示： 1-16条， 共(.*?)条", text)
if len(book_count_parse) > 0:
    book_num = int(book_count_parse[0])

# book_num = 282
# print(bookCount)
pages = math.ceil(book_num / 16) +1
# print(type(pages))
# print(pages)
# pages = 12
for i in range(1, pages):
    # print(i)
    pagination_link = "https://www.amazon.cn/s/ref=sr_pg_{}?{}&page={}".format(i, query, i)
    # print(pagination_link)
    parse_page_book(pagination_link,header)
