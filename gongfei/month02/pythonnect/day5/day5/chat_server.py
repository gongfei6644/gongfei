# -*- coding:utf-8 -*-
"""
Chat room server
env: python3.5
exc: for socket and fork 
"""

from socket import * 
import os,sys 

# 服务端地址
ADDR = ('0.0.0.0',8888)
# 存储用户
user = {}

# 搭建网络连接
def udp_server():
    # 创建套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    return s 

def do_login(s,name,addr):
    if name in user:
        s.sendto("该用户已存在".encode(),addr)
        return 
    s.sendto(b'OK',addr)
    
    # 通知其他人
    msg = "欢迎 %s 进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    # 加入字典
    user[name] = addr

def request(s):
    while True:
        data,addr = s.recvfrom(1024)
        msgList = data.decode().split(' ')
        # 区分请求类型
        if msgList[0] == 'L':
            do_login(s,msgList[1],addr)


if __name__ == "__main__":
    s = udp_server()
    request(s) # 接收请求

