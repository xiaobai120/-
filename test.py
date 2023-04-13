import requests
import aiohttp
import asyncio
from lxml import etree
import aiofiles
import time


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
del iurl_list[60]
del iurl_list[60]
# del iurl_list[93]
for iurl in iurl_list:
    iresp=requests.get(iurl)
    iresp.encoding=iresp.apparent_encoding
    ihtml=etree.HTML(iresp.text)
    AID=str(ihtml.xpath('//*[@id="dtl"]/div[1]/input/@value'))[2:11]
    CID=str(ihtml.xpath('//*[@id="dtl"]/div[2]/input/@value'))[2:11]
    surl=f'https://api.bilibili.com/x/player/playurl?avid={AID}&cid={CID}&qn=1&type=&otype=json&platform=html5&high_quality=1'
    dic=requests.get(surl,headers=headers).json()
    #print(iurl_list.index(iurl),dic)
    vurl_list.append(dic['data']['durl'][0]['url'].replace('\u0026','&'))#拿到vurl部分
    iresp.close()

async def dowmload_mp4(url,session):
    vedioname = str(vurl_list.index(url) ) + '.mp4'
    #
   #aiohttp.ClientSession() == requests
    async with session.get(url,headers=headers) as resp:
        async with aiofiles.open("mp4/" + vedioname, mode="wb") as f:
            await f.write(await resp.content.read())  # 异步读取内容


async def main():
    tasks=[]
    async with aiohttp.ClientSession() as session:
        for url in vurl_list:
            tasks.append(asyncio.create_task(dowmload_mp4(url,session)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main())
    #asyncio.run(main())
    loop.close()

