from socket import *
import os,sys 

# 服务器地址
ADDR = ('127.0.0.1',8888)

def udp_client():
    return socket(AF_INET,SOCK_DGRAM)

def login(s):
    while True:
        name = input("请输入姓名:")
        msg = "L " + name # L表示请求类型
        # 给服务器发送
        s.sendto(msg.encode(),ADDR)
        # 等待回复
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break 
        else:
            print(data.decode())

if __name__ == "__main__":
    s = udp_client()
    login(s)