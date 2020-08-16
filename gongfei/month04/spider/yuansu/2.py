import requests
def login():
    url = "http://www.51yuansu.com/"
    data = {
        "action": "user_login",
        "user_login":"9280310@qq.com",
        "user_pass": '9280310cjc',
    }
    response = requests.post(url,data)
    cookie = response.cookies.get_dict()
    print(cookie)
    # url2 ="http://www.jobbole.com/bookmark/"
    # response2 = requests.get(url2,cookies=cookie)
    # print(response2.text)


login()