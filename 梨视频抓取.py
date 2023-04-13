import requests
from lxml import etree

url=input("请输入你要的视频链接:")
#url='https://www.pearvideo.com/video_1752341' 示例url链接
cont_id=url.split("_")[1]

statusurl=f'https://www.pearvideo.com/videoStatus.jsp?contId={cont_id}&mrd=0.05405535117360416'

headers={
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Referer": url,#防盗链反爬
}
resp=requests.get(statusurl,headers=headers)

dic=resp.json()

srcurl=dic['videoInfo']['videos']['srcUrl']
systemTime=dic['systemTime']

srcurl=srcurl.replace(systemTime,f'cont-{cont_id}')
#print(srcurl)
with open("first.mp4",mode="wb") as f:
    f.write(requests.get(srcurl).content)
print("done!!")
resp.close()

