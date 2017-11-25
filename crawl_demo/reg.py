# coding=utf-8
import re

side ="""
        <ul id="ref_658394051" data-typeid="n">
     <li class="shoppingEngineExpand">
                                        <a href="/s/ref=lp_658394051_ex_n_1?rh=n%3A658390051&amp;bbn=658390051&amp;ie=UTF8&amp;qid=1511514550"><span class="srSprite backArrow"></span><span>图书</span></a>
                                    </li>
                                <li style="margin-left: 8px">
                                        <strong>文学</strong>
                                    </li>
                                <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_0?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">文学理论</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_1?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658509051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">文学评论与鉴赏</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_2?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658510051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">文学史</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_3?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658511051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">名家作品及欣赏</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_4?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658512051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">作品集</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_5?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658515051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">散文随笔</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_6?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A2126308051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">影视文学</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_7?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658516051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">诗歌词曲</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_8?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658517051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">纪实文学</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_9?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A2147365051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">戏剧与曲艺</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_10?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658519051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">民间文学</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_11?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658520051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">期刊杂志</span>
                             </a>
                          </li>
            <li style="margin-left: 6px">
                      <a href="/s/ref=lp_658394051_nr_n_12?fst=as%3Aoff&amp;rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A663149051&amp;bbn=658394051&amp;ie=UTF8&amp;qid=1511514550&amp;rnid=658394051">
                             <span class="refinementLink">文学作品导读</span>
                             </a>
                          </li>
            </ul>
              
"""


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
r = re.findall('<a href="(/s/ref=lp_\d+_nr_n_[\d+].*?)>.*?<span class="refinementLink">(.*?)</span>.*?</a>', side, re.S|re.M)
# print(r)
# print(len(r))

from collections import namedtuple
result = namedtuple('result',['link', 'title'])




for i in r:
    a, b = i
    print(a,b)
    # result(*i)
    # print(i)
# print(result)
# for x in result:
    # print(x)

