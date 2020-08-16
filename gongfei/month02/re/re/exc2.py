import re
import sys

port = sys.argv[1]  #　获取命令行输入端口名

f = open('1.txt')

#　找ｐｏｒｔ对应段落
while True:
    data = ''
    for line in f:
        #　如果不是空行
        if line != '\n':
            data += line
        else:
            break
    #　文档结尾
    if not data:
        print('No port')
        break

    # 查看段落首个单词是否为ｐｏｒｔ
    try:
        PORT = re.match(r'\S+',data).group()
    except Exception:
        continue

    if port == PORT:
        # pattern = r"[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}"
        pattern=r"(\d{1,3}\.){3}\d{1,3}/\d+|Unknown"
        address = re.search(pattern,data).group()
        print(address)
        break

f.close()






