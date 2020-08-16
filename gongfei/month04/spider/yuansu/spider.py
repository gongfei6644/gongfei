import requests
headers = {
        "Cookie": "Hm_lvt_671285ec519ac6bb9fa932b238ce1f32=1592725580,1592727197; _ref=http%3A%2F%2Fwww.51yuansu.com%2Fsearch%2F0-7-0-0-0-1%2F; sid=6232b7941e878da0901103be4b368a8b; uid=vrnfjgxoh%7CShmily; _patm=1592990386; _reurl=http%3A%2F%2Fwww.51yuansu.com%2Fsearch%2F0-7-0-0-0-1%2F; 51YSSSID=dscvjtcrfrnbcuvqjk6qm80hk7; Hm_lpvt_671285ec519ac6bb9fa932b238ce1f32=1592734417",
        "Referer": "http://www.51yuansu.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

# res = requests.get(url='http://www.51yuansu.com/index.php?m=ajax&a=down&id=vcrtyguyun',headers=headers)
#
# print(res.json())

# http://down.51yuansu.com/pic3/00/62/61/58105e9f3610a605f633e4ddc831c03f.png?auth_key=1592732959-0-0-0666c85e05ba6bd620c2d091a5e258fe

# proxy_url = "https://api.xiaoxiangdaili.com/ip/get?appKey=591940448109875200&appSecret=4Bpey8hw&cnt=1&wt=json"
#
# res = requests.get(url=proxy_url)
# print(res.json().get('data')[0].get('ip'))

url = "http://pic.51yuansu.com/pic3/cover/03/97/53/5df32e36642c2_610.jpg"

res = requests.get(url=url)
print(res.content)
with open('test.jpg','wb') as f:
    f.write(res.content)