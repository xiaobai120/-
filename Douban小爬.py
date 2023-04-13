import re
import requests

url = "https://movie.douban.com/top250"
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}
resp=requests.get(url,headers=headers)

page_content= resp.text
# print(resp.status_code)

obj = re.compile(r'<li>.*?<div class="item">.*?<em class="">(?P<ID>\d+)</em>.*?<span class="title">(?P<name>.*?)</span>.*?导演: (?P<director>.*?)\s.*?(?P<year>\d{4}).*?<span class="rating_num" property="v:average">(?P<score>\d.\d)</span>',re.S)
iter = obj.finditer(page_content)
for i in iter:
    print("电影排名:",i.group("ID"),"电影名称:",i.group("name"),"导演:",i.group("director"),"年份:",i.group("year"),"得分:",i.group("score"))
resp.close()