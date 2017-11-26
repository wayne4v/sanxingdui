from urllib.parse import urljoin

u1 = "https://www.amazon.cn/s/ref=lp_658390051_nr_n_0?fst=as:off&rh=n:658390051,n:!658391051,n:658394051&bbn=658391051&ie=UTF8&qid=1511664262&rnid=658391051"
u2 = "https://www.amazon.cn/s/ref=lp_658394051_nr_n_1/460-9538982-4165717?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658509051&bbn=658394051&ie=UTF8&qid=1511665740&rnid=658394051"
u3 = urljoin(u1, u2)
print(u3)