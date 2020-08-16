import re
import traceback
import base64
import requests
import json
from urllib.parse import quote, unquote
from lxml import etree
from requests.exceptions import ProxyError

from utils.common_logger import get_logger


def get_response(url):
    burl = base64.b64encode(url.encode("gb2312"))
    uurl = quote(burl)
    referer = "http://search.fang.com/captcha-verify/redirect?h={}".format(url)
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        "cache-control": "no-cache",
        # "referer": referer,
        # "cookie": cookie,

    }
    # host = url[8:].split("/")[0] if url.startswith("https") else url[7:].split("/")[0]
    # headers['Host'] = host
    # headers["Accept-Language"] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'



    proxy = 'http://HZ6G1XLV727H0R3D:B853A793BA6EF2D1@http-dyn.abuyun.com:9020'
    proxies = {"http": proxy, "https": proxy}
    for i in range(50):
        try:

            resp = requests.get(url, headers=headers, timeout=30, verify=False)
            print("code: ", resp.status_code)
            print(url)
            print(resp.url)
            print(resp.content.decode("utf-8", "ignore"))
            if resp.status_code == 200 and url == resp.url.replace("esf1", "esf"):
                print(11111)
                return resp
        except ProxyError as e:
            print("第{}次请求, {}".format(i, e))
        except Exception as e:
            print("异常{}{}".format(e, traceback.format_exc()))
    else:
        print("50次失败")

def parse(resp):
    # print(resp.text)
    text = resp.content.decode("utf-8", "ignore")
    html = etree.HTML(text)
    # r = html.xpath('//span[contains(text(), "二手房房源")]/following-sibling::a[1]/text()')
    # print([resp.text])
    # data = json.loads(resp.text)
    # r = data['comm_propnum']['saleNum']
    r = html.xpath('//ul[@id="listTableBox"]/li')
    # print(text)
    print(1111111111111111)
    print(resp.content.decode("utf-8", "ignore"))
    print(2222222222222)




def main():
    url = "https://esf.fang.com/chushou/3_437456629.htm"
    # url = "https://sz.esf.fang.com/chushou/3_219906392.htm?_rfss=1"
    response = get_response(url)
    print(response.status_code, response.url)
    if response.status_code == 200:
        parse(response)
        with open("ttttt.html", "wb") as f:
            f.write(response.content)



# "https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam&serialID=c90831a2b36d4e63c6c95c55796e8237_249572c642604441856dd17af4b6a093&history={}"
# "https://qd.anjuke.com/community/view/303186"
# if "captcha-verify" in req_url:
        #     real_url = req_url.split("history=")[-1]
# base64_url = unquote("c90831a2b36d4e63c6c95c55796e8237_249572c642604441856dd17af4b6a093")
# print(base64_url)
# req_url = base64.b64decode(base64_url).decode("utf-8")
# print(req_url)

logger = get_logger("test", "房天下二手房", "/log")




if __name__ == '__main__':
    main()
    pass