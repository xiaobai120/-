import re
import requests

url='https://www.dytt89.com/'#初始网页

resp=requests.get(url)# verify = False 去掉安全验证

#解决乱码
resp.encoding=resp.apparent_encoding # apparent_encoding会从网页的内容中分析网页编码的方式,解决乱码问题
resp.encoding='gb2312' # 看html源码看其编码方式自己指定字符集

page_content= resp.text

obj1=re.compile(r'2022必看热片.*?<ul>(?P<ul>.*?)<ul>',re.S)
result=obj1.finditer(page_content)
for it in result:
    ul=it.group("ul")#作为下次匹配的字符集
obj2=re.compile(r"<li><a href='(?P<ul2>.*?)'",re.S)
result2=obj2.finditer(ul)#在html中a标签表示超链接

url_lst=[]
for i in result2:
    url_lst.append(url+i.group("ul2").strip('/'))

obj3=re.compile(r'◎片　　名　(?P<movie>.*?)<br />.*?'
                r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<dowmload>.*?)"',re.S)
for itt in url_lst:
    resp1=requests.get(itt)
    resp1.encoding=resp1.apparent_encoding
    result3=obj3.search(resp1.text)
    print(result3.group("movie"))
    print(result3.group("dowmload"))
resp.close()
resp1.close()