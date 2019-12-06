from django.shortcuts import render
from .models import Users
from .models import LifedataComplete
from .models import Lifedata2
from django.db.models import Sum
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponse
from .check_code import create_validate_code
from io import BytesIO

# # Create your views here.
def check_code(request):
    """
    获取验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    # 生成图片 img、数字代码 code，保存在内存中，而不是 Django 项目中
    img, code = create_validate_code()
    img.save(stream, 'PNG')

    # 写入 session
    request.session['valid_code'] = code
    return HttpResponse(stream.getvalue())

def loginproc(request):
    return render(request,'login.html')

def dologin(request):

    #根据标签的name获取用户输入信息。
    user = request.POST.get('user',None)
    passwd = request.POST.get('passwd',None)

    # 获取用户输入的验证码
    code = request.POST.get('check_code')
    p = request.POST.get('p')
    with open('logindata.txt','a+') as f:
        f.write("{}-{}".format(user,passwd))
    if user=="":
        return render(request,'login.html',{'ret':['请输入账号!']})

    try:
        correct_passwd = Users.objects.get(userid = user).passwd
    except:
        return render(request,'login.html',{'ret':['无效的账号!']})

    if code.upper() == request.session.get('valid_code').upper():
        if correct_passwd==passwd:
            view1_lst1,view1_lst2 = view1_func('2018-10-30')
            view2_lst1,view2_lst2,view2_lst3,view2_lst4 = view2_func('10')
            view3_lst1,view3_lst2,view3_lst3 = view3_func('10')
            lst1,lst2,lst3,lst4 = view4_1_func('10')
            record,alert = warning_func()
            return render(request,'government.html',{'view1_lst1':view1_lst1,'view1_lst2':view1_lst2,\
                        'view2_lst1':view2_lst1,'view2_lst2':view2_lst2,'view2_lst3':view2_lst3,'view2_lst4':view2_lst4,\
                        'view3_lst1':view3_lst1,'view3_lst2':view3_lst2,'view3_lst3':view3_lst3,\
                        'lst1': lst1+lst3, 'lst2': lst2,'lst4':lst4,'record':record,'alert':alert,'user':user})
        else:
            return render(request,'login.html',{'ret':['账号或密码错误']})
    else:
        return render(request, 'login.html',{'ret':['验证码错误']})


def logout(request):
    response = HttpResponse('logout!!!')
    #清除cookie里保存的username
    response.delete_cookie('passwd')
    response.delete_cookie('user')

    return render(request, 'login.html')

def view1_func(date):
    lifedata = Lifedata2.objects.filter(create_time__contains = date)
    detail = lifedata.values('event_property_name').annotate(Count("event_property_name"))
    view1 = list(detail)
    temp1,temp2 = [],[]
    for one in view1:
        temp1.append(one['event_property_name'])
    for i in range(len(temp1)):
        temp2.append({'value':view1[i]['event_property_name__count'],'name':temp1[i]})
    return temp1,temp2


def view1(request):
    if request.is_ajax():
        date = request.GET.get('date')
        view1_lst1,view1_lst2 = view1_func(date)
        return JsonResponse({'view1_lst1':view1_lst1,'view1_lst2':view1_lst2},charset='utf-8',json_dumps_params={'ensure_ascii':False})

def view2_func(month):
    lifedata = Lifedata2.objects.filter(create_time__regex=r'.+-.*{}-+'.format(month))
    detail = lifedata.values('street_name').annotate(Count("street_name"))
    view2 = list(detail)
    view2_lst1,view2_lst2,view2_lst3,view2_lst4 = [],[],[],[]
    temp = []
    for one in view2:
        view2_lst1.append(one['street_name'])
    for i in range(len(view2_lst1)):
        view2_lst2.append(view2[i]['street_name__count'])
    for j in range(len(view2_lst1)):
        num_lst = lifedata.filter(street_name=view2_lst1[j]).values('event_type_name').annotate(Count("event_type_name"))
        num_lst = list(num_lst)
        temp.append(num_lst)

    if temp==[]:
        return None,None,None,None

    for item in temp[0]:
        view2_lst3.append(item['event_type_name'])

    for event in view2_lst3:
        mytemp = []
        for street in view2_lst1:
            mytemp.append(lifedata.filter(street_name=street).filter(event_type_name=event).count())
        view2_lst4.append(mytemp)
    return view2_lst1,view2_lst2,view2_lst3,view2_lst4

def view2(request):
    #特定月份下的民生事件情况
    if request.is_ajax():
        month = request.GET.get('month',None)
        month = int(month)
        view2_lst1,view2_lst2,view2_lst3,view2_lst4 = view2_func(month)
        return JsonResponse({'view2_lst1':view2_lst1,'view2_lst2':view2_lst2,'view2_lst3':view2_lst3,'view2_lst4':view2_lst4},\
                            charset='utf-8',json_dumps_params={'ensure_ascii':False})

def view3_func(month):
    lifedata = Lifedata2.objects.filter(create_time__regex=r'.+-.*{}-+'.format(month))
    detail = lifedata.values('community_name').annotate(Count("community_name"))
    view3 = list(detail)
    temp1, temp2,temp3,temp = [],[],[],[]
    for one in view3:
        temp1.append(one['community_name'])
    for i in range(len(temp1)):
        temp2.append(view3[i]['community_name__count'])
        temp.append((view3[i]['community_name'],view3[i]['community_name__count']))
    temp = sorted(temp,key=lambda x:x[1],reverse=True)
    i = 0
    for one in temp:
        i += 1
        if(i>10):
            break
        temp3.append({one[0]:one[1]})
    return temp1,temp2,temp3

def view3(request):
    if request.is_ajax():
        month = request.GET.get('month', None)
        month = int(month)
        view3_lst1,view3_lst2,view3_lst3 = view3_func(month)
        return JsonResponse( {'view3_lst1': view3_lst1, 'view3_lst2': view3_lst2,'view3_lst3':view3_lst3},\
                                charset='utf-8',json_dumps_params={'ensure_ascii':False})

def view4_1_func(month):
    month=int(month)
    lifedataComplete = Lifedata2.objects.filter(create_time__regex = r'.+-.*{}-+'.format(month))

    # 不同处理情况的个数
    a = lifedataComplete.aggregate(overtime_archive_num = Sum('overtime_archive_num'))
    b = lifedataComplete.aggregate(intime_to_archive_num = Sum('intime_to_archive_num'))
    c = lifedataComplete.aggregate(intime_archive_num = Sum('intime_archive_num'))


    temp1 = ["超期结办", "处理中", "按期结办"]
    temp2 = []
    for one in a.keys():
        key = one
        break
    temp2.append({'value':a[key],'name':'超期结办'})
    for one in b.keys():
        key = one
        break
    temp2.append({'value':b[key],'name':'处置中'})
    for one in c.keys():
        key = one
        break
    temp2.append({'value':c[key],'name':'按期结办'})

    # 不同处理情况及具体时间的个数
    detail = lifedataComplete.values('event_type_name').annotate(Count("event_type_name"))
    detail = list(detail)
    temp3,temp4 = [],[]
    for one in detail:
        temp3.append(one['event_type_name'])
    for i in range(len(temp3)):
        temp4.append({'value':detail[i]['event_type_name__count'],'name':temp3[i]})
    return temp1,temp2,temp3,temp4

def view4_1(request):
    #根据用户选择的日期实现可视化功能4
   if request.is_ajax():
        """访问数据库获得数据并传回前端"""
        month = request.GET.get('month',None)

        """根据特定月份问题处理情况"""
        lst1,lst2,lst3,lst4=view4_1_func(month)
        return JsonResponse( {'lst1': lst1+lst3, 'lst2': lst2,'lst4':lst4},\
                                charset='utf-8',json_dumps_params={'ensure_ascii':False})

def view4_2(request):
    if request.is_ajax():
        """访问数据库获得数据并传回前端"""
        quarter = request.GET.get('quarter', None)
        quarter = int(quarter)
        lifedataComplete_quarter = Lifedata2.objects.filter(create_time__regex=r'.+-.*{}-+'.format(int(quarter * 3 - 2))) | \
                                   Lifedata2.objects.filter(create_time__regex=r'.+-.*{}-+'.format(int(quarter * 3 - 1))) | \
                                   Lifedata2.objects.filter(create_time__regex=r'.+-.*{}-+'.format(int(quarter * 3)))
        # 以下是特定季度内的接办情况
        a3 = lifedataComplete_quarter.aggregate(overtime_archive_num=Sum('overtime_archive_num'))
        b3 = lifedataComplete_quarter.aggregate(intime_to_archive_num=Sum('intime_to_archive_num'))
        c3 = lifedataComplete_quarter.aggregate(intime_archive_num=Sum('intime_archive_num'))

        # 以下是特定季度范围内的详细信息
        lst1 = ["超期结办", "处理中", "按期结办"]
        lst23 = []
        for one in a3.keys():
            key = one
            break
        lst23.append({'value': a3[key], 'name': '超期结办'})
        for one in b3.keys():
            key = one
            break
        lst23.append({'value': b3[key], 'name': '处置中'})
        for one in c3.keys():
            key = one
            break
        lst23.append({'value': c3[key], 'name': '按期结办'})

        # 不同处理情况及具体时间的个数
        detail3 = lifedataComplete_quarter.values('event_type_name').annotate(Count("event_type_name"))
        detail3 = list(detail3)
        lst33, lst43 = [], []
        for one in detail3:
            lst33.append(one['event_type_name'])
        for i in range(len(lst33)):
            lst43.append({'value': detail3[i]['event_type_name__count'], 'name': lst33[i]})

        return JsonResponse( {'lst1':lst1+lst33,'lst2': lst23, 'lst4': lst43},\
                                charset='utf-8',json_dumps_params={'ensure_ascii':False})

def view4_3(request):
    if request.is_ajax():
        startDate = request.GET.get('startDate', None)
        endDate = request.GET.get('endDate', None)
        if startDate>endDate:
            return JsonResponse({'lst1':[],'message':'请选择正确的时间范围!'},\
                                charset='utf-8',json_dumps_params={'ensure_ascii':False})
        if startDate==endDate:
            lifedataComplete2 = Lifedata2.objects.filter(create_time__contains=startDate)
        else:
            lifedataComplete2 = Lifedata2.objects.filter(create_time__gte=startDate).filter(create_time__lte=endDate)
        # 以下是特定时间范围内的接办情况
        a2 = lifedataComplete2.aggregate(overtime_archive_num=Sum('overtime_archive_num'))
        b2 = lifedataComplete2.aggregate(intime_to_archive_num=Sum('intime_to_archive_num'))
        c2 = lifedataComplete2.aggregate(intime_archive_num=Sum('intime_archive_num'))

        # 以下是特定时间范围内的详细信息
        lst1 = ["超期结办", "处理中", "按期结办"]
        lst22 = []
        for one in a2.keys():
            key = one
            break
        lst22.append({'value': a2[key], 'name': '超期结办'})
        for one in b2.keys():
            key = one
            break
        lst22.append({'value': b2[key], 'name': '处置中'})
        for one in c2.keys():
            key = one
            break
        lst22.append({'value': c2[key], 'name': '按期结办'})

        # 不同处理情况及具体时间的个数
        detail2 = lifedataComplete2.values('event_type_name').annotate(Count("event_type_name"))
        detail2 = list(detail2)
        lst32, lst42 = [], []
        for one2 in detail2:
            lst32.append(one2['event_type_name'])
        for i in range(len(lst32)):
            lst42.append({'value': detail2[i]['event_type_name__count'], 'name': lst32[i]})
        return JsonResponse({'lst1':lst1+lst32,'lst2': lst22, 'lst4': lst42},\
                                charset='utf-8',json_dumps_params={'ensure_ascii':False})

def warning_func():
     LifedataComplete2 =LifedataComplete.objects.filter(create_time__contains="2018/10/30")
     LifedataComplete3 =LifedataComplete.objects.filter(
         event_type_name="党纪政纪")& LifedataComplete.objects.filter(overtime_archive_num=1)&LifedataComplete.objects.filter(create_time__contains="2018/10")
     record = []
     N = LifedataComplete2.count()
     for i in range(N):
         temp = []
         temp.append(LifedataComplete2[i].create_time)
         temp.append(LifedataComplete2[i].street_name)
         temp.append(LifedataComplete2[i].community_name)
         temp.append(LifedataComplete2[i].event_src_name)
         temp.append(LifedataComplete2[i].event_type_name)
         temp.append(LifedataComplete2[i].event_property_name)
         temp.append(LifedataComplete2[i].dispose_unit_name)
         record.append(temp)
     alert = []
     M= LifedataComplete3.count()
     for i in range(M):
         temp = []
         temp.append(LifedataComplete3[i].create_time)
         temp.append(LifedataComplete3[i].street_name)
         temp.append(LifedataComplete3[i].community_name)
         temp.append(LifedataComplete3[i].event_src_name)
         temp.append(LifedataComplete3[i].event_type_name)
         temp.append(LifedataComplete3[i].event_property_name)
         temp.append(LifedataComplete3[i].dispose_unit_name)
         alert.append(temp)
     return record,alert

