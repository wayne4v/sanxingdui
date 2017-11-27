# crawl amazcon.cn

## install
1. touch config_cralw.ini to your '~' dir

##参考资料
http://blog.csdn.net/u013055678/article/details/54172693
http://blog.csdn.net/kwsy2008/article/details/48372665
https://www.cnblogs.com/wang-yc/p/5693288.html

https://www.cnblogs.com/huangxincheng/p/5002794.html

入队列时用lpush，拿数据时用brpop
BLPOP指令可以在队列为空时处于阻塞状态。就不用处于轮询的状态。 //消费者只需从队列中LPOP任务，如果为空则轮询。
http://blog.csdn.net/men_wen/article/details/62237970
##TIPS
python3.6 -m pip install --upgrade pip setuptools wheel