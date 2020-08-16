import re

html = '''
<div class="animal">
    <p class="name">
		<a title="Tiger"></a>
    </p>
    <p class="content">
		Two tigers two tigers run fast
    </p>
</div>

<div class="animal">
    <p class="name">
		<a title="Rabbit"></a>
    </p>

    <p class="content">
		Small white rabbit white and white
    </p>
</div>
'''

pattern = re.compile('<div class="animal">.*?title="(.*?)".*?content">(.*?)</p>',re.S)
r_list = pattern.findall(html)

for r in r_list:
    print('动物名称:',r[0].strip())
    print('动物描述:',r[1].strip())
    print('*'*50)
# [
#     ('Tiger', 'Two tigers'),
#     ('Rabbit', 'Small white rabbit ')
# ]









