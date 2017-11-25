# coding=utf-8
import re
from collections import namedtuple
import requests
def response(url, headers):
    rep = requests.get(url, headers=headers)
    return rep.text

import random

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


if __name__ == '__main__':
    url1 = 'https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=sa_menu_top_books_l1?ie=UTF8&node=658390051'
    url2 = 'https://www.amazon.cn/s/ref=lp_658390051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051&bbn=658391051&ie=UTF8&qid=1511598696&rnid=658391051'
    url3 = 'https://www.amazon.cn/s/ref=lp_658394051_nr_n_0?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051&bbn=658394051&ie=UTF8&qid=1511598711&rnid=658394051'

    headers = {
        'User-Agent': FakeChromeUA.get_ua(),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    # print(headers)
    # print(html)
    html = response(url3, headers=headers)
    html_1 = '''
        
                      <a href="/s/ref=lp_658390051_nr_n_0?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051" target="_blank">
                             <span class="refinementLink">文学</span>
                             </a>
                          
     <li style="margin-left: 0px">
                                        <strong>图书</strong>
                                    </li>
                                <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_0?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051" target="_blank">
                             <span class="refinementLink">文学</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_1?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658393051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">小说</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_2?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658396051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">传记</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_3?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658403051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">青春动漫</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_4?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658395051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">艺术与摄影</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_5?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658409051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">少儿</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_6?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658683051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">家庭教育</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_7?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658405051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">孕产育儿</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_8?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A118362071&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">社会科学</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_9?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658424051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">哲学与宗教</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_10?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658415051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">政治与军事</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_11?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658417051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">心理学</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_12?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658418051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">历史</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_13?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658416051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">法律</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_14?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658423051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">国学</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_15?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658399051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">经济管理</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_16?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658397051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">励志与成功</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_17?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658400051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">考试辅导</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_18?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658410051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">外语学习</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_19?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A305884071&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">中小学教辅</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_20?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A120837071&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">大中专教材</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_21?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658437051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">辞典与工具书</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_22?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658431051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">科技</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_23?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658429051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">科学与自然</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_24?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658414051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">计算机与互联网</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_25?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658428051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">医学</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_26?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658408051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">旅游与地图</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_27?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658407051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">烹饪美食与酒</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_28?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658401051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">时尚</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_29?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658673051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">运动健身</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_30?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658411051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">恋爱与婚姻</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_31?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658406051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">家居手工休闲</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_32?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658402051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">娱乐</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_33?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658404051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">养生保健</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_34?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658433051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">体育</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_35?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658438051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">期刊杂志</span>
                             </a>
                          </li>
            <li style="margin-left: -2px">
                      <a href="/s/ref=lp_658390051_nr_n_36?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A2045366051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511598696&amp;rnid=658391051">
                             <span class="refinementLink">进口原版</span>
                             </a>
                          </li>
            
    '''
    # print(html)
    categories = re.findall('<a href="(/s/ref=lp_\d+_nr_n_[\d+].*?)>.*?<span class="refinementLink">(.*?)</span>.*?</a>', html, re.S|re.M)
    # print(categories)
    print(len(categories))
    for c in categories:
        a, b = c
        print(a, b)
# /s/ref=lp_658390051_nr_n_15?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658399051&amp;bbn=658391051&amp;ie=UTF8&amp;qid=1511507310&amp;rnid=658391051
# r = re.findall("/http://www.amazon.cn*/", side)
# r = re.findall(r'(<li style="margin-left: 6px"><a href="/s/ref=lp_\d+_nr_n_\d+?.*">.*</a></li>)', side)
# patter = re.compile(r'''(?i)href=["']([^\s"'<>]+)''')
# r = patter.match(side)
# print(len(r))
# r = re.findall(r'''(?i)href=["']([^\s"'<>]+)''', side)
# r = re.findall(r'''(?i)href=["'](/s/ref=lp_\d+_nr_n_\d+[^\s"]+)''', side)
# r = re.findall('href="(/s/ref=lp_[\d+].*?)">', side)
# r = re.findall(r'''^<li><.*>(.*)</a></li>$''', side)

# r = re.findall(r"""(?i)href=["']([^\s"'<>]+)""", side)
# r = pattern.match(side)
# r = re.findall(r'''<a href=.*?>(.*?)</a>''', side)
# reg = re.compile('<span.*?>(.*?)</span>')
# reg = re.compile(''''\<li*?<\/li>''')
# r = re.findall(reg, side)
# print(r)
# print(len(r))
# with open('/Users/vavne/Desktop/zcn/demo/x.htm', 'rb') as f:
#     doc = f.read()

# print(doc)
# print(doc.encode('itf-8'))

# print(r)
# print(len(r))

# result = namedtuple('result',['link', 'title'])
#
# ''''''
#
# for i in r:
#     a, b = i
#     print(a,b)
    # result(*i)
    # print(i)
# print(result)
# for x in result:
    # print(x)

