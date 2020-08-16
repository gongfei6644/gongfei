import json

import decimal
from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def addcart_views(request):
  if request.method == 'POST':
    #从session中获取登录信息并转换成UserInfo对象
    user = UserInfo() # 模拟从session中获取出来的并转换成UserInfo对象的登录信息
    # 获取goodsid,colorid,sperid,amount
    goodsid = request.POST.get('goodsid')
    colorid = request.POST.get('colorid')
    sperid = request.POST.get('sperid')
    amount = request.POST.get('amount')
    # 通过以上的id们得到对应的对象,再获取相应的值
    try:
      goods = Goods.objects.get(id=goodsid)
      goodcolor = GoodsColor.objects.get(id=colorid)
      goodspe = GoodsDetail.objects.get(id=sperid)
    except Exception as ex:
      retDic = {
        "result":False,
        "data":"",
        "error":"异常"
      }
      return HttpResponse(json.dumps(retDic))
    #查询是否有相同的用户,商品,规格,颜色的购物车记录,如果有的话则实现的是数量的累加,如果没有则增加至数据库
    oldcart = Cart.objects.filter(user_id=user.id,goods_id=goodsid,color=goodcolor.color,spec=goodspe.specifice)
    if oldcart:
      #已经存在该商品再购物车,只做数量更新即可
      oldcart[0].amount = oldcart[0].amount + int(amount)
      oldcart[0].save() # 更新
    else:
      #将数据保存进购物车
      new_cart = Cart()
      new_cart.user = user
      new_cart.goods = goods
      new_cart.color = goodcolor.color
      new_cart.spec = goodspe.specifice
      new_cart.price = decimal.Decimal(goods.price)
      new_cart.amount = int(amount)
      new_cart.save()

    retDic = {
      "result":True,
      "data":"",
      "error":""
    }
    return HttpResponse(json.dumps(retDic))

def cartlist_views(request):
  if request.method == 'GET':
    # 从session中将用户的信息获取出来
    user = UserInfo() # 模拟从session中获取出来的session信息
    # 将user用户所有的在购物车内的商品获取出来
    find_carts = Cart.objects.filter(user_id=user.id)
    # 获取每个商品的标题,图片,颜色,规格,价格,数量,商品id,购物车id
    cart = []
    for fc in find_carts:
      cart_good = {}
      cart_good['title'] = fc.goods.title
      cart_good['img'] = str(fc.goods.listimg)
      cart_good['color'] = fc.color
      cart_good['spec'] = fc.spec
      cart_good['price'] = fc.price
      cart_good['amount'] = fc.amount
      cart_good['goodid'] = fc.goods.id
      cart_good['cartid'] = fc.id
      cart.append(cart_good)
    retDic = {
      'result' : True,
      'data' : cart,
      'error': ''
    }
    return HttpResponse(json.dumps(retDic))













