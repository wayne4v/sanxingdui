import re

from test.av import AvGot as av

ROOT = "https://movie.douban.com/tag/"

# 正则：类别地址与类别名称
reTag = re.compile('<a href="(\/tag\/.*?)">(.*?)<\/a>')
# 正则：详情页面链接及电影标题
reLinkTitle = re.compile('<a href="(https:\/\/movie\.douban\.com\/subject\/\d+/)".*?>([\s\S]*?)<\/a>')
# 正则：电影时长及评分
reRuntimeRate = re.compile('<span property="v:runtime" content="(\d+)">[\s\S]*?<strong class="ll rating_num" property="v:average">(.*?)<\/strong>')

@av.entry(ROOT, reTag)
async def entry_callback(results):
  # 构造列表页地址
  return list(map(lambda row: ("https://movie.douban.com{}".format(row[0]), row[1]), result))

# @av.register(reLinkTitle)
# async def list_page(result):
#   # 显示未清理前结果
#   print(result)
#   def clean(row):
#     return (row[0], re.sub(r'<.*?>|\s', "", row[1]))
#   return list(map(clean, result))

# @av.register(reRuntimeRate)
# async def detail_page(result):
#   print(result)

av.run()
av.close()