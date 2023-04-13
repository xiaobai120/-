import requests
from lxml import etree
import threading
from  threading import Thread
from concurrent.futures import ThreadPoolExecutor

url="https://www.bilibili.com/v/popular/rank/all"
resp=requests.get(url)

html=etree.HTML(resp.text)
resp.close()
li_list=html.xpath('//*[@id="app"]/div/div[2]/div[2]/ul/li')

url_list=[]#li部分url
iurl_list=[]#i链接url
vurl_list=[]#视频源url

for li in li_list:
    url_list.append(str(li.xpath("./div/div[2]/a/@href")).replace('/','',2))#拿到url部分
for urll in url_list:
    iurl_list.append('http://www.i'+urll[6:-2])#拿到iurl部分

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

# #删除用不了的url
# del iurl_list[4]
# del iurl_list[93]
del iurl_list[60]
for iurl in iurl_list:
    iresp=requests.get(iurl)
    iresp.encoding=iresp.apparent_encoding
    ihtml=etree.HTML(iresp.text)
    AID=str(ihtml.xpath('//*[@id="dtl"]/div[1]/input/@value'))[2:11]
    CID=str(ihtml.xpath('//*[@id="dtl"]/div[2]/input/@value'))[2:11]
    surl=f'https://api.bilibili.com/x/player/playurl?avid={AID}&cid={CID}&qn=1&type=&otype=json&platform=html5&high_quality=1'
    dic=requests.get(surl,headers=headers).json()
    print(iurl_list.index(iurl),dic)
    vurl_list.append(dic['data']['durl'][0]['url'].replace('\u0026','&'))#拿到vurl部分
    #print(dic['data']['durl'][0]['url'].replace('\u0026','&'))
    iresp.close()

#第一种:直接下载(慢的一逼)
# for vurl in vurl_list:
#     vedioname=str(vurl_list.index(vurl)+7)+'.mp4'
#     #print(requests.get(vurl,).status_code)
#     with open("mp41/"+vedioname,mode="wb") as f:
#          f.write(requests.get(vurl,headers=headers).content)


#第二种:简单多线程(快一点点)
# def func(urllist):
#     for url in urllist:
#         vedioname = str(vurl_list.index(url) ) + '.mp4'
#         with open("mp4/"+vedioname,mode="wb") as f:
#             f.write(requests.get(url,headers=headers).content)
#
# class Mythread(Thread):
#     def __init__(self,urllist):
#         threading.Thread.__init__(self)
#         self.url_list=urllist
#
#     def run(self):
#         func(self.url_list)
#
# if __name__ == '__main__':
#     t1 = Mythread(vurl_list[0:20]).start()
#     t2 = Mythread(vurl_list[20:40]).start()
#     t3 = Mythread(vurl_list[40:60]).start()
#     t4 = Mythread(vurl_list[60:80]).start()
#     t5 = Mythread(vurl_list[80:99]).start()


#第三种:线程池(更快一点点)
# def func(url):
#     vedioname = str(vurl_list.index(url) ) + '.mp4'
#     with open("mp4/"+vedioname,mode="wb") as f:
#         f.write(requests.get(url,headers=headers).content)
#
# if __name__ == '__main__':
#     with ThreadPoolExecutor(10) as t:
#         for url in vurl_list:
#             t.submit(func,url)

