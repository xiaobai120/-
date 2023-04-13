import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.127 Mobile Safari/537.36; ; zjxw; 8.3.3; 00000000-67e8-b8c7-0000-00005a3e4c8d; M2012K11AC 20,9; Android; 12; zh; xiaomi",
    "cookie": "PHPSESSID=uc1kqqgjd0i3p2fbotg58plbv3; Hm_lvt_2bdcd4007f59360aa8457d7135541070=1651155571; acw_tc=2f624a4b16511905589651726e410942fc0e1779ed7f1bbbf5547c714f15b0; Hm_lpvt_2bdcd4007f59360aa8457d7135541070=1651190560",
    "Content-Type": "multipart/from-data;boundary=----WebKitFormBoundary9lrJyyWylbMrRBft",
}
# 开始答题

resp = requests.get(
    url="https://lrhgysoz.act.tmuact.com/activity/api.php?m=front&subm=answer&action=answerinfo&answer_id=1510&answer_start=1",
    headers=headers,
)
print(resp.text)

# 答题中
for i in range(500):
    resp = requests.get(
        url="https://lrhgysoz.act.tmuact.com/activity/api.php?m=front&subm=answer&action=answerinfo&answer_id=1510&page="
        + str(i + 1),
        headers=headers,
    )
    dic = resp.json()
    id = str(dic["data"]["list"][0]["id"])
    win_id = str(dic["data"]["list"][0]["win_id"])
    last = "0"
    if i == 499:
        last = "1"
    payload = MultipartEncoder(
        fields={
            "id": (id),
            "option": ('["' + win_id + '"]'),
            "yongshi": ("1"),
            "last": (last),
        },
        boundary="------WebKitFormBoundary9lrJyyWylbMrRBft",
    )
    headers["Content-Type"] = payload.content_type
    resp = requests.post(
        url="https://lrhgysoz.act.tmuact.com/activity/api.php?m=front&subm=answer&action=answerdata&answer_id=1510",
        data=payload,
        headers=headers,
    )
    dic = resp.json()
    end_id = str(dic["data"]["id"])
    # 结束答题
    if end_id != "0":
        resp = requests.post(
            url="https://lrhgysoz.act.tmuact.com/activity/api.php?m=front&subm=answer&action=answerresult&answer_id=1510&id="
            + end_id,
            data=payload,
            headers=headers,
        )
        print(resp.text)
    print(resp.text, i + 1)
