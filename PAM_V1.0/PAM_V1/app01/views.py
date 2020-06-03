from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Create your views here.


def register(request):
    return render(request, 'register.html')


def doregister(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    db = pymysql.connect('localhost', 'root', 'lf',
                         'family_bill', charset='utf8mb4')

    cursor = db.cursor()
    sql = 'select account_number from users'
    cursor.execute(sql)
    data = cursor.fetchall()
    data = [i[0] for i in data]
    if username in data:
        db.close()
        return HttpResponse("<h1 style='color:red;margin:0 auto;margin-top:10%;text-align:center'>账号已存在,请返回重新注册</h1>")
    else:
        cursor2 = db.cursor()
        sql = 'insert into users value(null,{},{})'.format(username, password)
        cursor.execute(sql)
        db.commit()
        db.close()
        return HttpResponse("<h1 style='color:red;margin:0 auto;margin-top:10%;text-align:center'>注册成功</h1>")


def login(request):
    return render(request, 'login.html')


def do_main(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    # 创建数据库连接对象
    db = pymysql.connect('localhost', 'root', 'lf',
                         'family_bill', charset='utf8mb4')

    cursor = db.cursor()
    sql = 'select account_number,password from users'
    cursor.execute(sql)
    data = cursor.fetchall()
    if tuple((username, password)) in data:
        return main(request)
    else:
        return redirect('/', {'wrong': '您输入的账号或密码错误'})


def main(request):
    db = pymysql.connect('localhost', 'root', 'lf', 'family_bill',
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    sql = 'select id,name,category,time,money from main order by time desc;'
    res = cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return render(request, 'main.html', {'data': data})


def append(request):
    db = pymysql.connect('localhost', 'root', 'lf', 'family_bill',
                         charset='utf8mb4')
    cursor = db.cursor()
    cust_id = request.POST.get('cust_id')
    name = request.POST.get('name')
    category = request.POST.get('category')
    if category == '请选择类别':
        return HttpResponse('<h3>格式不正确</h3><ul><li>编号是数字,不重复于其他项目.</li><li>名称不为空,在10个字符内.</li><li>您是否选择了类别?</li><li>时间格式示例:2020-03-05</li><li>金额处填写数字,不要带中文,英文,符号等.</li></ul>')
    time = request.POST.get('time')
    money = request.POST.get('money')
    sql = 'insert into main values ({},"{}","{}","{}",{})'.format(cust_id,
                                                                  name, category, time, money)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return redirect('/main/')
    except:
        db.rollback()
        db.close()
        return HttpResponse('<h3>格式不正确</h3><ul><li>编号是数字,不重复于其他项目.</li><li>名称不为空,在10个字符内.</li><li>您是否选择了类别?</li><li>时间格式示例:2020-03-05</li><li>金额处填写数字,不要带中文,英文,符号等.</li></ul>')


def remove(request):
    db = pymysql.connect('localhost', 'root', 'lf', 'family_bill',
                         charset='utf8mb4')
    cursor = db.cursor()
    cust_id = request.POST.get('remove_id')
    sql = 'delete from main where id ={}'.format(cust_id)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return redirect('/main/')
    except:
        db.rollback()
        db.close()
        return HttpResponse('请检查格式是否正确')


def to_analysis_main(request):
    engine = create_engine(
        'mysql+pymysql://root:lf@localhost:3306/family_bill')
    plt.style.use('seaborn')
    plt.rcParams['font.family'] = ['Arial Unicode MS',
                                   'Microsoft Yahei', 'SimHei', 'sans-serif']
    data = pd.read_sql('select * from main', engine, index_col='id')
    data = data[['category', 'money']]
    data = data.groupby('category').sum()
    plt.pie(data[['money']], labels=data.index)
    plt.savefig('static/images/tmp.jpg')
    plt.clf()
    return redirect('/analysis_main/')


def analysis_main(request):
    return render(request, 'analysis_main.html')


