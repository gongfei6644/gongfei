import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def goodetail_views(request):
  """
  读取某商品的详情信息
  :param request: 请求对象
  :return: 包含某商品具体信息的JSON串
  """
  if request.method == 'GET':
      goodid = request.GET.get('goodid')
      good = Goods.objects.filter(id=goodid)[0]
      #获取good对应的详细信息(大图,小图,名,描述,价格,规格,颜色)
      #获取商品所有图片 - GoodsImg
      goodimg = good.goodsimg_set.all()
      #获取商品所有详情 - GoodsDetail
      gooddetail = good.goodsdetail_set.all()
      #获取商品所有颜色 - GoodsColor
      goodcolor = good.goodscolor_set.all()

      # 处理产品对应的图像
      bigimg=[] # 大图列表
      smallimg=[] # 小图列表
      for img in goodimg:
        bigimg.append(str(img.goodsimgbig))
        smallimg.append(str(img.goodsimg))

      # 处理gooddetail
      spelist = []
      for detail in gooddetail:
        spe = {}
        spe["id"] = detail.id
        spe["spicifice"] = detail.specifice
        spelist.append(spe)

      #　处理goodcolor
      colorlist = []
      for gcolor in goodcolor:
        col = {}
        col['id'] = gcolor.id
        col['color'] = gcolor.color
        colorlist.append(col)

      #将查询出来的商品的所有信息封装到一个字典中
      godetail = {}
      godetail['title'] = good.title
      godetail['price'] = str(good.price)
      godetail['desc'] = good.desc
      godetail['promise'] = serializers.serialize("json",good.promise.all())
      godetail['bigimg'] = bigimg
      godetail['smallimg'] = smallimg
      godetail['spelist'] = spelist
      godetail['colorlist'] = colorlist

      respDic = {
        'result':True,
        'data':godetail,
        'error':"",
      }

      return HttpResponse(json.dumps(respDic))











