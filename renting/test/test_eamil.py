import unittest
import requests
from utils import statistics_send_email as email


class EmailTestCase(unittest.TestCase):
     def test_email(self):
          url = 'http://127.0.0.1:8888/static/email'
          headers = {}
          res = requests.get(url,headers= headers)
          msg = res.text
          email.send(msg, '租房每日采集量统计报告')
