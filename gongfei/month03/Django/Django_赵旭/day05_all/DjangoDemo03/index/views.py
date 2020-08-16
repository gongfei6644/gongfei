from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Sum, Avg, Count, F


# Create your views here.
def parent_views(request):
    uname = "吕泽Maria"
    return render(request,'01-parent.html',locals())

def child_views(request):
    uname = "小泽老师"
    return render(request,'02-child.html',locals())

def create_views(request):
    #方案1:Entry.objects.create()
    # au1 = Author.objects.create(name="老魏",age=44,email='laowei@163.com')

    #方案2:obj.save()
    # obj = Author(name="蒙蒙")
    # obj.age = 18
    # obj.email = "mengmeng@163.com"
    # obj.save()

    #方案3:obj.save()
    dic = {
        "name" : "WangDB",
        "age" : 36,
        "email" : "wangdb@163.com",
        "isActive" : False
    }

    obj = Author(**dic)
    obj.save()
    print("ID:%s,姓名:%s,年龄:%s,邮箱:%s,激活:%s" % (obj.id,obj.name,obj.age,obj.email,obj.isActive))

    return HttpResponse("增加数据成功")

def retrieve_views(request):
    # 1.查看Entry.objects的类型
    # ret = Author.objects
    # print("Author.objects:",ret)
    # print("Author.obejcts的类型:",type(ret))

    # 2.all(): 查询所有数据,并查看返回值
    # authors = Author.objects.all()
    # print(authors)
    # print("authors的类型:",type(authors))
    # for au in authors:
    #     print("ID:%s,姓名:%s,年龄:%s,邮箱:%s,激活:%s" % (au.id,au.name,au.age,au.email,au.isActive))

    # 3.values():查询返回部分列的信息
    # authors = Author.objects.values()
    # for au in authors:
    #     print("姓名:%s,邮箱:%s" % (au['name'],au['email']))

    # 4.values_list():查询返回部分列的信息
    # authors = Author.objects.values_list("name","email")
    # print(authors)

    return HttpResponse("查询成功")


def filter_views(request):
    # 1. 查询 id=1的 Author的信息
    # ret = Author.objects.filter(id=1)

    # 2. 查询id=1并且name=小泽Maria的Author的信息
    # authors = Author.objects.filter(
    #     id=1,
    #     name='吕泽Maria'
    # )
    # if authors:
    #     for au in authors:
    #         print("姓名:%s,邮箱:%s" % (au.name,au.email))
    # else:
    #     print("查询的数据不存在")

    # 3.查询年龄大于30的Author的信息们
    # Author.objects.filter(age>30) # 此写法错误

    # 4.查询name中包含字符a的Author的信息
    # authors = Author.objects.filter(name__contains="a")

    # 5.查询年龄在30-40之间的Author的信息
    authors = Author.objects.filter(age__range=(30,40))

    for au in authors:
        print("姓名:%s,年龄:%s,邮箱:%s" % (au.name,au.age,au.email))

    return HttpResponse("查询成功")

def filterexer_views(request):
    # 1.查询出age大于等于30的所有的Author
    authors = Author.objects.filter(age__gte=30)
    # 2.查询出所有姓"吕"的Author
    authors = Author.objects.filter(name__startswith="吕")
    # 3.查询出Email中包含ao的所有Author
    authors = Author.objects.filter(email__contains='ao')
    # 4.查询出书籍的出版时间在1990~2000年之间的图书信息
    books = Book.objects.filter(publicate_date__year__range=(1990,2000))
    # 5.查询出Author中年龄大于吕泽Maria年龄的Author的信息
    # 5.1 查询出吕泽Maria的年龄
    # result = Author.objects.filter(name='吕泽Maria').values('age')
    # 5.2 查询出Author中age大于result的Author们
    # authors = Author.objects.filter(age__gt=result)
    # 5.3 以上两个步骤合二为一
    Author.objects.filter(
        age__gt = Author.objects.filter(
            name='吕泽Maria'
        ).values('age')
    )

    for au in authors:
        print("姓名:%s,年龄:%s,邮箱:%s" % (au.name,au.age,au.email))

    return HttpResponse("查询成功")

def exclude_views(request):
    authors = Author.objects.exclude(id=1)

    for au in authors:
        print("ID:%s,姓名:%s,年龄:%s,邮箱:%s" % (au.id,au.name,au.age,au.email))

    return HttpResponse("Query OK")

def get_views(request):
    # 1.查询id=1的Author的信息
    # author = Author.objects.get(id=1)
    # print(author.name)

    # 2.查询id=9的Author的信息
    # authors = Author.objects.get(id=9)
    # 以上抛异常,因为查询不到数据
    return HttpResponse("查询成功")


def aggregate_views(request):
    # from django.db.models import Sum,Avg
    # 1.查询Author中所有人的年龄的总和和平均值
    # result = Author.objects.aggregate(
    #     avgAge = Avg('age'),
    #     sumAge = Sum('age')
    # )
    #
    # print("平均年龄:%.2f,总年龄:%d" % (result['avgAge'],result['sumAge']))

    # 2.查询年龄大于30的人的平均年龄和人数
    # result = Author.objects.filter(
    #     age__gt=30).aggregate(
    #     avgAge = Avg('age'),
    #     count = Count('*')
    # )
    # print(result)

    # 3.查询Author中每个isActive下的人数
    result = Author.objects.values('isActive').annotate(count=Count('*'))

    for r in result:
        print("组:%s,人数:%d" % (r['isActive'],r['count']))
    return HttpResponse("聚合函数查询成功")


def queryall_views(request):
    #1.筛选出isActive为True的所有的Author信息
    authors = Author.objects.filter(isActive=True)
    #2.渲染到10-queryall.html模板上
    return render(request,'10-queryall.html',locals())

def querybyid_views(request,id):
    author = Author.objects.get(id=id)
    return render(request,'11-querybyid.html',locals())


def delete_views(request,id):
    # 1.修改id对应的Author的isActive为False
    try:
        au = Author.objects.get(id=id)
        au.isActive = False
        au.save()
    except Exception as e:
        print(e)
    # 2.重定向回10-queryall
    return redirect('/10-queryall')

def updateall_views(request):
    Author.objects.all().update(age=F('age')+10)
    return HttpResponse('更新成功')

def oto_views(request):
    #1.向wife表中增加数据
    #1.1 通过外键属性关联数据
    # wife = Wife()
    # wife.wname = "吕夫人Maria"
    # wife.wage = 16
    # wife.author_id = 1 #关联wife与author
    # wife.save()

    #1.2 通过关联属性关联数据
    # author = Author.objects.get(id=2)
    # wife = Wife()
    # wife.wname = '魏夫人'
    # wife.wage = 40
    # wife.author = author
    # wife.save()

    #1.3 查询"魏夫人"以及对应的Author的信息
    # wife = Wife.objects.get(wname='魏夫人')
    # print("夫人姓名:%s,夫人年龄:%s,Author姓名:%s,Author年龄:%s" % (wife.wname,wife.wage,wife.author.name,wife.author.age))
    #1.4 查询"吕泽Maria"以及对应的Wife的信息
    author = Author.objects.get(name='吕泽Maria')
    print("Author姓名:%s,Wife姓名:%s" % (author.name,author.wife.wname))

    return HttpResponse("查询成功")

def otm_views(request):
    #查询 清华大学出版社所出版的书籍们
    pub = Publisher.objects.get(name='清华大学出版社')
    # 获取pub对应的所有的书籍信息
    books = pub.book_set.all()

    print("出版社:",pub.name)
    print("书籍:")
    for book in books:
        print("书名:%s,出版时间:%s" % (book.title,book.publicate_date))

    return HttpResponse("查询数据成功")


def otmexer_views(request,pid):
    # pid 表示的是要查看的publisher的id
    # 1.查询所有的publisher
    publishers = Publisher.objects.all()
    # 2.查询所有的book
    books = Book.objects.all()
    # 根据pid的值来判断查询所有书籍还是按条件查询书籍
    if pid:
        pid = int(pid)
        if pid > 0:
            #按条件筛选book的信息
            # 方式1:通过pid直接查询books
            # books = Book.objects.filter(publisher_id = pid)

            # 方式2:通过pid先查询publisher,再通过publisher查询books
            publisher = Publisher.objects.get(id=pid)
            books = publisher.book_set.all()
    return render(request,'16-otm-exer.html',locals())

def mtm_views(request):
    # 将老魏 与 清华大学出版社 关联到一起
    # author = Author.objects.get(name='老魏')
    # publisher = Publisher.objects.get(name__startswith='清华大学出版社')
    # author.publishers.add(publisher)

    # 1.查询author中id为4的Author所对应的出版社
    # author = Author.objects.get(id=4)
    # pubs = author.publishers.all()
    # print("作者姓名:",author.name)
    # print("签约出版社:")
    # for pub in pubs:
    #     print("出版社名称:",pub.name)
    # 2.查询publisher中id为1的出版社对应的作者们
    pub = Publisher.objects.get(id=1)
    authors = pub.author_set.all()
    print("出版社名称:",pub.name)
    print("签约作者:")
    for au in authors:
        print("作者姓名:",au.name)

    return HttpResponse("查询数据成功")





