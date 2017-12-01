import requests
import re
import html

def response_content(isbn):
    pass
    
def parse_sale(url):
    rep = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
    text = rep.text

    book_title_p = '''<span id="productTitle" class="a-size-large">(.*?)</span>'''
    book_title = re.findall(book_title_p, text)
    print(html.unescape(book_title[0]))

    hot_sale_p = '''图书商品里排第(.*?)名 '''
    tmp = re.findall(hot_sale_p, text)
    print(tmp[0])

    sale_li_p = '''<ul class="zg_hrsr">(.*?)</ul>'''
    sale_li_html = re.findall(sale_li_p, text, re.S | re.M)
    parse_sale_test(sale_li_html[0])


def parse_sale_test(sale_li_html):
    pattern_rank_category = '''<span class="zg_hrsr_rank">第(.*?)位</span>'''
    rank_c = re.findall(pattern_rank_category, sale_li_html)
    pattern_category = '''<a href=".*?">([\u4e00-\u9fff]+)</a>'''
    results = re.findall(pattern_category, sale_li_html, re.S | re.M)
    from itertools import groupby
    rank_gorup = [list(group) for k, group in groupby(results, lambda x: x == "图书") if not k]
    rg = dict(zip(rank_c, rank_gorup))
    for k, rank_sale in rg.items():
        ss = ("第{}位, 图书 - {}").format(k, ' > '.join(rank_sale))
        print(ss)

if __name__ == '__main__':
    # parse_content("9787501243754")
    a = "https://www.amazon.cn/%E4%B8%96%E7%95%8C%E5%90%84%E5%9B%BD%E5%9F%8E%E5%BE%BD%E9%9B%86%E9%94%A6-%E5%BC%A0%E5%B0%8F%E5%B7%9D/dp/B00AQU8RU4/ref=sr_1_1/459-3192124-1551857?ie=UTF8&amp;qid=1512091663&amp;sr=8-1&amp;keywords=9787501243754"
    parse_sale(a)
    # parse_sale_test()
