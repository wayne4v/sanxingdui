from collections import namedtuple

import aiohttp
import asyncio
import re

# Task 所需要携带的属性
Node = namedtuple("Node", ["url", "re", "callback"])

class AvGot(object):
  _ENTRY = "ENTRY_NODE"
  def __init__(self, loop=None):
    self._prev_node = None
    self.pipe = {}

    # 异步任务队列
    self.queue = asyncio.Queue()
  def entry(self, url="", regexp=""):
    def wrapper(callback):
      node = Node(url, regexp, callback)
      if self.pipe.get(self._ENTRY) is None:
        self.pipe[self._ENTRY] = node
      else:
        # 以 Cleaning 函数而不是 node 作为 Key
        # 因为任务队列中需要构造新的 node
        self.pipe[self.prev_node.callback] = node
      self._prev_node = node
    return wrapper
  def register(self, regexp=r''):
    """
     除入口页面
     其他页面地址 url 依赖上级页面提取结果
    """
    return self.entry("", regexp)

  def run(self):
    # 将入口页面放入队列
    self.queue.put_nowait(self.pipe.get(self._ENTRY))

    async def _runner():
      producer = asyncio.ensure_future(self._worker())
      await self.queue.join()
      producer.cancel()

    self.loop.run_until_complete(_runner())


  async def _worker():
    while True:
      node = self.queue.get()

      # Cleaning 函数在这里回调，并产生下一级页面入口
      results = await node.callback(await self.extract(node.url, node.re))

      if results is not None:
        for page in results:
          # 从 pipe 链表中取出下一级的 node
          p = self.pipe.get(node.callback)
          if p is not None:
            # 根据结果中的 url 构造新的任务并放回到队列里
            next_node = Node(page[0], p.re, p.callback)
            self.queue.put_nowait(next_node)
      self.queue.task_done()
#以上就是异步爬虫的基本结构，有一点需要约定好的是所有的  Cleaning 方法必须以列表形式返回清洗之后的结果，且下一级页面入口必须在第一位（最后一页除外）。接下来做一个简单的测试，以豆瓣电影分类页面为入口，进入该类别列表，最后进入电影详情页面，并提取电影时长和评分：

