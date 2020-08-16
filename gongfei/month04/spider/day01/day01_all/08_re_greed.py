import re

html = '''
<html>
    <div><p>成也风云</p></div>
    <div><p>败也风云</p></div>
</html>
'''
# 贪婪匹配
pattern = re.compile('<div><p>.*</p></div>',re.S)
r_list = pattern.findall(html)

# 非贪婪匹配
pattern = re.compile('<div><p>(.*?)</p></div>',re.S)
r_list = pattern.findall(html)
print(r_list)

















