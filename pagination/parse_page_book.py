import requests
import html
import re
url = "https://www.amazon.cn/s/ref=sr_pg_1?rnid=664971051&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658393051%2Cn%3A658495051%2Cp_36%3A100-2000&qid=1511960661&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&bbn=658495051&low-price=1&high-price=10&x=0&y=0&page=1"
rep = requests.get("url")
text = rep.text
pattern = '''<a class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal" target="_blank" title="(.*?)" href="(.*?)">.*?</a>'''
books = re.findall(pattern, text)
# print(books)
for info in books:
    title, link = info
    print("title:{}, link:{}".format(html.unescape(title), link))