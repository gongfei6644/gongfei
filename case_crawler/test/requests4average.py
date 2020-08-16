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
    cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; budgetLayer=1%7Cbj%7C2019-06-18%2014%3A21%3A27; resourceDetail=1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; __utmc=147393320; __utmz=147393320.1562934211.33.19.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/; Captcha=54424F47374E786264774E523870554A6C6367363442334A57532B4A676E6377487836486A496B66726B744E3739722B6D4F456C676A326F7342655A355A7346344B4B77335654306344303D; newhouse_chat_guid=43F0A0FB-EA25-9129-D97D-FC1C6A4025D1; city=sz; __utma=147393320.3500232.1560338584.1563071182.1563153028.35; g_sourcepage=esf_xq%5Elb_pc; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; unique_cookie=U_haxkax8249tj5zdl5h0tp1j9l1jjy02o0dx*44; __utmb=147393320.42.10.1563153028"
    # cookie = "global_cookie=858rxappvbibay2xvvj0knhnj2zjpdnfwnn; Integrateactivity=notincludemc; lastscanpage=0; newhouse_user_guid=8F79FB4C-E7E7-A82F-1EAB-80A740138AA1; budgetLayer=1%7Cbj%7C2019-06-18%2014%3A21%3A27; resourceDetail=1; searchConN=1_1562072520_529%5B%3A%7C%40%7C%3A%5Db2755e4c34cf6f19bdf36bf7f5e7f252; vh_newhouse=1_1562135369_1723%5B%3A%7C%40%7C%3A%5Dc986ba3e7921e9c51a1d863325527852; new_search_uid=6beab057a77eed00b3111dba591ed79b; __utmc=147393320; __utmz=147393320.1562934211.33.19.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/captcha-verify/; Captcha=54424F47374E786264774E523870554A6C6367363442334A57532B4A676E6377487836486A496B66726B744E3739722B6D4F456C676A326F7342655A355A7346344B4B77335654306344303D; newhouse_chat_guid=43F0A0FB-EA25-9129-D97D-FC1C6A4025D1; city=sz; __utma=147393320.3500232.1560338584.1563071182.1563153028.35; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; __utmb=147393320.57.10.1563153028; unique_cookie=U_haxkax8249tj5zdl5h0tp1j9l1jjy02o0dx*56"


    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
        # "cache-control": "no-cache",
        # "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        # "upgrade-insecure-requests": "1",
        # "pragma": "no-cache",
        # "referer": referer,
        # "cookie": cookie
    }


    proxy = 'http://HZ6G1XLV727H0R3D:B853A793BA6EF2D1@http-dyn.abuyun.com:9020'
    proxies = {"http": proxy, "https": proxy}
    for i in range(50):
        try:
            resp = requests.get(url, headers=headers, proxies=proxies)
            print("code: ", resp.status_code)
            print(url)
            print(resp.url)
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
    text = resp.content.decode("utf-8", "ignore")
    html = etree.HTML(text)
    # r = html.xpath('//span[contains(text(), "二手房房源")]/following-sibling::a[1]/text()')
    # print([resp.text])
    # data = json.loads(resp.text)
    # r = data['comm_propnum']['saleNum']
    r = html.xpath('//span[@class="price"]/text()')
    # print(text)
    print(r)





def main():
    url = "https://qd.58.com/xiaoqu/xixiangyuanqd/"
    # url = "https://ynyl.esf.fang.com/housing/15416_20255_1_0_0_0_1_0_0_0/?_rfss=1"
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


"""

"""

logger = get_logger("test", "房天下二手房", "/log")




if __name__ == '__main__':
    main()
    pass