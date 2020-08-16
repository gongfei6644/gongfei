import requests
import time
import random
import string

class BilibiVideoSpider(object):
    def __init__(self):
        self.url = 'http://api.vc.bilibili.com/board/v1/ranking/top?'
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        self.all_chars = string.punctuation + string.whitespace

    # 获取jsonxiangying
    def get_json(self):
        for offset in range(1,32,10):
            params = {
                'page_size': '10',
                'next_offset': str(offset),
                'tag': '今日热门',
                'platform': 'pc'
            }
            
            html = requests.get(
                url=self.url,
                params=params,
                headers=self.headers
            ).json()
            self.downloader(html)

    # 下载视频
    def downloader(self,html):
        # 提取列表
        for video in html['data']['items']:
            # 视频链接
            video_url = video['item']['video_playurl']
            # 名字
            video_name = video['item']['description']
            # 发请求保存视频
            # 处理video_name中的特殊字符,文件名有时会报错
            for char in video_name:
                if char in self.all_chars:
                    video_name = video_name.replace(char,'')

            # 文件名不能超过255个字符(ubuntu中)
            if len(video_name) >= 50:
                video_name = video_name[:51]

            filename = video_name + '.mp4'
            video_content = requests.get(
                video_url,headers=self.headers
            ).content
            
            with open(filename,'wb') as f:
                f.write(video_content)
                print('%s下载成功' % filename)
            
            time.sleep(random.randint(2,5))
            
if __name__ == '__main__':
    spider = BilibiVideoSpider()
    spider.get_json()
    
    
    
    
    
    
    
    
    
    
    
    
    
