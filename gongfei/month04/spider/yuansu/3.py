import os
import time
import requests
from lxml import etree

ABY_URI = ''


def get_headers():
    headers = {
        # "Cookie": "Hm_lvt_671285ec519ac6bb9fa932b238ce1f32=1592725580,1592727197; _ref=http%3A%2F%2Fwww.51yuansu.com%2Fsearch%2F0-7-0-0-0-1%2F; 51YSSSID=2mgfv0705f0ijn8a1gbdma7mi2; sid=6232b7941e878da0901103be4b368a8b; uid=vrnfjgxoh%7CShmily; _patm=1592990386; _reurl=http%3A%2F%2Fwww.51yuansu.com%2Fsearch%2F0-7-0-0-0-1%2F; Hm_lpvt_671285ec519ac6bb9fa932b238ce1f32=1592731353",
        "Referer": "http://www.51yuansu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    auth_key = str(int(time.time()))+"-0-0-577f41ae2f9ce907989a465c679a354e"

    return headers


def save_images(content,file_name):
    print("file_name",file_name)
    with open(file_name,'wb') as f:
        f.write(content)

def down(url,proxy=''):
    headers = get_headers()
    if proxy:
        res = requests.get(url=url, headers=headers,proxies={'http':proxy, 'https': proxy},verify=False)
    else:
        res = requests.get(url=url, headers=headers)
    return res

def get_title_url():
    url = "http://www.51yuansu.com/all/"
    res = down(url)
    html = etree.HTML(res.text)
    items = html.xpath('/html/body/div[2]/div[3]/div/div/ul/li')[1:]

    title_url_list = []
    for item in items:
        url_dict = {}
        title = item.xpath('./a/text()')[0]
        children = item.xpath('./div/a')
        url_dict[title] = {}
        if len(children) == 1:
            url = children[0].xpath('./@href')[0]
            url_dict[title]["全部"] = url
        else:
            for child in children:
                name = child.xpath('./text()')[0]
                name = name.replace('/', '_')
                if name != "全部":
                    url = child.xpath('./@href')[0]
                    url_dict[title][name] = url
        title_url_list.append(url_dict)

    print(title_url_list)
    return title_url_list

def deal_url(title_url_list):
    for item in title_url_list:
        print('item',item)
        for key, value in item.items():
            for k,v in value.items():
                title = key
                t = k
                url = v
                path = os.path.join(os.getcwd(), title+'/'+t)
                print(1, path)
                if not os.path.exists(path):
                    os.makedirs(path)
                url = url.split('-')[0:-1]
                url = '-'.join(url)
                for i in range(1,251):
                    url_ = url + '-'+ str(i) + '/'
                    # print(url_)
                    res = down(url_)
                    deal_message(res.text, path)

def deal_message(content,path):
    html = etree.HTML(content)
    if html:
        items = html.xpath('//*[@id="f-content"]/div')
        for item in items:
            src = item.xpath('./div[@class="img-out-wrap"]/a/img/@data-src')[0]
            src = src.split('!')[0]
            print('src',src)
            id = item.xpath('./div[@class="i-p-op"]/div[@class="i-op-d"]/a/@data-id')[0]
            print('id:',id)

            ip_time = proxy_ip.get('time')
            if ip_time and time.time() - ip_time > 10:
                proxy_ = get_ip()
                proxy_ip['ip'] = proxy_
                proxy_ip['time'] = time.time()
            proxy = proxy_ip.get('ip')

            try:
                res = requests.get(url=src, proxies={'http': proxy, 'https': proxy}, timetout=20)
                time.sleep(0.1)
                print('ttt:',res.content)
                file_name = os.path.join(path, str(id) + '.jpg')
                save_images(res.content, file_name)
            except Exception as e:
                print("连接异常",e)


            # file_name = os.path.join(path, str(id)+'.jpg')
            # url = 'http://www.51yuansu.com/index.php?m=ajax&a=down&id={}'.format(id)
            # ip_time = proxy_ip.get('time')
            # if ip_time and time.time() - ip_time > 10:
            #     proxy_ = get_ip()
            #     proxy_ip['ip'] = proxy_
            #     proxy_ip['time'] = time.time()
            # proxy = proxy_ip.get('ip')
            # res = down(url,proxy).json()
            # res = down(url).json()
            # print(res)
            # time.sleep(10)

            # url = res.get('url')
            # print('aaa:',url)
            # if url:
            #     res1 = down(url)
            #     save_images(res1.content, file_name)


def main():
    title_url_list = get_title_url()
    deal_url(title_url_list)


def get_ip():
    proxy_url = "https://api.xiaoxiangdaili.com/ip/get?appKey=591940448109875200&appSecret=4Bpey8hw&cnt=1&wt=json"
    res_proxy = requests.get(url=proxy_url).json()
    print('rr:',res_proxy)
    ip = res_proxy.get('data')[0].get('ip')
    port = res_proxy.get('data')[0].get('port')
    proxy = ip+":"+str(port)
    print('proxy:',str(proxy))
    return proxy

if __name__ == '__main__':
    prox = get_ip()
    proxy_ip = {"ip": prox, "time":time.time()}
    main()
