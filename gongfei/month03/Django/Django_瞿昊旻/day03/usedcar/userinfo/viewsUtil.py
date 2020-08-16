from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import random
import io

def rndColor():
    C1 = random.randint(0,255)
    C2 = random.randint(0,255)
    C3 = random.randint(0,255)
    return (C1,C2,C3)

def verifycode(request):
    bgcolor = '#997679'
    width = 100
    height = 25
    im = Image.new('RGB', (width,height), bgcolor)
    draw = ImageDraw.Draw(im)

    numb_1 = {"1":"壹","2":"er","3":"san","4":"si","5":"wu","6":"liu","7":"qi","8":"ba","9":"jiu"}
    numb_2 = random.randint(1,50)
    sign = ["+","-"]
    numb_1_n = random.randrange(1,10)
    numb_1_s =str(numb_1_n)
    first_s = numb_1[numb_1_s]
    third_s = str(numb_2)
    sign_n = random.randrange(0,2)
    second_s = sign[sign_n]
    if sign_n == 0:
        last = numb_1_n +numb_2
    else:
        last = numb_2 - numb_1_n
    last_s = str(last)

    font = ImageFont.truetype('/usr/share/fonts/truetype/fonts-japanese-gothic.ttf',23)
    draw.text((5,2),'?',font=font,fill=rndColor())
    draw.text((20,2),second_s,font=font,fill=rndColor())
    draw.text((35,2),first_s,font=font,fill=rndColor())
    draw.text((60,2),'=',font=font,fill=rndColor())
    draw.text((75,2),last_s,font=font,fill=rndColor())

    draw.point()
    draw.line()
    del draw




    buf = io.BytesIO()
    im.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')