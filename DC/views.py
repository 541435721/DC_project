# coding:utf-8
from django.shortcuts import render, redirect
from DC import forms
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now, timedelta
import datetime
from django.db.models import Avg, Sum, Count, Aggregate
from DC import models
import json
from django.views.decorators.cache import cache_page
from django.core.cache import cache

shopping = ['POS消费', '水控消费', '车载消费', '余额转移', '支付交易', '圈存转账', '喜付电控转账', 'POS消费冲正', '交易冲正']
income = ['支付宝充值', '支付领取', '卡充值', '喜付下发', '加卡余额', '换卡加值', '卡充值冲正', '圈存补帐', '易支付充值', 'POS充值']
operations = ['卡冻结', '锁卡流水', '卡挂失', '卡解挂', '更新卡信息', '修改卡有效期', '卡片开户', '消费失败', '卡补办', '卡片销户', '坏卡登记添加', '卡密码修改',
              '换卡申请', '换卡', '卡解冻', '坏卡登记删除', '修改消费限额', ]


def is_login(func):
    def wapper(request):
        if request.user.is_authenticated():
            return func(request)
        else:
            return redirect('/')

    return wapper


# Create your views here.
def index(request):  # 主页
    login_form = forms.LoginForm()
    regist_forms = forms.Regist()
    return render(request, 'index.html', {'form1': login_form, 'form2': regist_forms})


def login(request):  # 登录
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_id']  # 接收表单信息
            password = form.cleaned_data['pass_word']
            try:
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)  # 用户登录
                return redirect('/welcome/')
            except:
                pass
        else:
            pass
    return redirect('/')


def regist(request):  # 注册
    if request.method == 'POST':
        form = forms.Regist(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_id']  # 接收表单信息
            password = form.cleaned_data['pass_word']

            try:
                User.objects.create_user(username=username, password=password)  # 系统中创建用户
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)  # 用户登录
                return redirect('/user/')
            except:
                pass
        else:
            pass
    return redirect('/')


@is_login
def logout(request):
    auth.logout(request)
    return redirect('/')


@is_login
@cache_page(60 * 15)
def user(request):
    params = {'user_name': request.user,
              'income': 0,
              'today_income': 0,
              'all_costs': 0,
              'today_costs': 0,
              'shopping_records': None,
              'week_cost': None,
              'week_income': None, }
    costs = models.Cost.objects.filter(user_id=request.user).values('price')

    shopping = ['POS消费', '水控消费', '车载消费', '余额转移', '支付交易', '圈存转账', '喜付电控转账', 'POS消费冲正', '交易冲正']
    income = ['支付宝充值', '支付领取', '卡充值', '喜付下发', '加卡余额', '换卡加值', '卡充值冲正', '圈存补帐', '易支付充值', 'POS充值']
    operations = ['卡冻结', '锁卡流水', '卡挂失', '卡解挂', '更新卡信息', '修改卡有效期', '卡片开户', '消费失败', '卡补办', '卡片销户', '坏卡登记添加', '卡密码修改',
                  '换卡申请', '换卡', '卡解冻', '坏卡登记删除', '修改消费限额', ]
    shopping_records = []
    all_shopping = costs.filter(consume_type__in=shopping)
    all_income = costs.filter(consume_type__in=income)
    if costs:
        params['all_costs'] = round(all_shopping.aggregate(Sum('price'))['price__sum'], 2)
        params['income'] = round(all_income.aggregate(Sum('price'))['price__sum'], 2)

        for item in shopping:
            try:
                mount = round(all_shopping.filter(consume_type=item).aggregate(Sum('price'))['price__sum'], 2)
                shopping_records.append(mount)
            except:
                shopping_records.append(0)
        params['shopping_records'] = json.dumps(shopping_records)

    today = now().date()

    weekends_index = today.weekday()

    week_cost = [0] * 7
    week_income = [0] * 7
    count = 0
    for i in range(weekends_index, -1, -1):
        start = today - timedelta(days=i)
        end = start + timedelta(days=1)
        today_costs = all_shopping.filter(shopping_time__range=(start, end))
        today_income = all_income.filter(shopping_time__range=(start, end))

        if today_costs:
            try:
                week_cost[count] = round(today_costs.aggregate(Sum('price'))['price__sum'], 2)
            except:
                pass
        if today_income:
            try:
                week_income[count] = round(today_income.aggregate(Sum('price'))['price__sum'], 2)
            except:
                pass

        count += 1
    params['today_costs'] = week_cost[weekends_index]
    params['today_income'] = week_income[weekends_index]
    params['week_income'] = json.dumps(week_income)
    params['week_cost'] = json.dumps(week_cost)

    return render(request, 'user.html', params)


@is_login
def welcome(request):
    params = {'user_name': request.user,
              }

    params['reward'] = models.Schoolarship.objects.filter(user_id=request.user)

    scores = models.Scores.objects.filter(user_id=request.user)
    years = list(scores.values('year').distinct().values_list('year'))
    scores_dic = {}
    for year in years:
        record = list(scores.filter(year=year[0]).order_by('semester').values_list('semester', 'course_id', 'score'))
        scores_dic[year[0]] = record

    params['scores'] = scores_dic
    params['width'] = 12 // len(scores_dic)



    return render(request, 'html/welcome.html', params)


@is_login
@cache_page(60 * 15)
def message_table(request):
    params = {'user_name': request.user,
              'messages': None}
    records = models.Messages.objects.filter(user_id=request.user, mount__gt=0).order_by('time').reverse()
    params['messages'] = records
    return render(request, 'html/message_table.html', params)


@is_login
@cache_page(60 * 15)
def message_chart(request):
    params = {'user_name': request.user,
              }
    records = models.Messages.objects.filter(user_id=request.user).order_by('time')
    ans = []
    for record in records:
        ans.append([int(record.time.strftime("%Y")), int(record.time.strftime("%m")), int(record.time.strftime("%d")),
                    record.mount])
    params['massages'] = json.dumps(ans)
    print(ans)
    return render(request, 'html/message_chart.html', params)


@is_login
@cache_page(60 * 15)
def job_table(request):
    params = {'user_name': request.user,
              'address': None,
              'salary': None,
              'json_address': None,
              'json_salary': None}
    records1 = models.Job.objects.exclude(address='').values('address').annotate(Count('address'))
    records2 = models.Job.objects.exclude(salary=None).values('salary').annotate(Count('salary'))
    params['address'] = records1
    params['salary'] = records2
    return render(request, 'html/job_table.html', params)


@is_login
@cache_page(60 * 15)
def job_chart(request):
    params = {'user_name': request.user,
              }

    params = {'user_name': request.user,
              'address': None,
              'salary': None,
              'json_address': None,
              'json_salary': None}
    records1 = models.Job.objects.exclude(address='').values('address').annotate(Count('address'))
    records2 = models.Job.objects.exclude(salary=None).values('salary').annotate(Count('salary'))
    records = models.Job.objects.exclude(address='').exclude(salary=None)

    params['address'] = records1
    params['salary'] = records2

    records4 = []

    cites = ['海门',
             '鄂尔多斯',
             '招远',
             '舟山',
             '齐齐哈尔',
             '盐城',
             '赤峰',
             '青岛',
             '乳山',
             '金昌',
             '泉州',
             '莱西',
             '日照',
             '胶南',
             '南通',
             '拉萨',
             '云浮',
             '梅州',
             '文登',
             '上海',
             '攀枝花',
             '威海',
             '承德',
             '厦门',
             '汕尾',
             '潮州',
             '丹东',
             '太仓',
             '曲靖',
             '烟台',
             '福州',
             '瓦房店',
             '即墨',
             '抚顺',
             '玉溪',
             '张家口',
             '阳泉',
             '莱州',
             '湖州',
             '汕头',
             '昆山',
             '宁波',
             '湛江',
             '揭阳',
             '荣成',
             '连云港',
             '葫芦岛',
             '常熟',
             '东莞',
             '河源',
             '淮安',
             '泰州',
             '南宁',
             '营口',
             '惠州',
             '江阴',
             '蓬莱',
             '韶关',
             '嘉峪关',
             '广州',
             '延安',
             '太原',
             '清远',
             '中山',
             '昆明',
             '寿光',
             '盘锦',
             '长治',
             '深圳',
             '珠海',
             '宿迁',
             '咸阳',
             '铜川',
             '平度',
             '佛山',
             '海口',
             '江门',
             '章丘',
             '肇庆',
             '大连',
             '临汾',
             '吴江',
             '石嘴山',
             '沈阳',
             '苏州',
             '茂名',
             '嘉兴',
             '长春',
             '胶州',
             '银川',
             '张家港',
             '三门峡',
             '锦州',
             '南昌',
             '柳州',
             '三亚',
             '自贡',
             '吉林',
             '阳江',
             '泸州',
             '西宁',
             '宜宾',
             '呼和浩特',
             '成都',
             '大同',
             '镇江',
             '桂林',
             '张家界',
             '宜兴',
             '北海',
             '西安',
             '金坛',
             '东营',
             '牡丹江',
             '遵义',
             '绍兴',
             '扬州',
             '常州',
             '潍坊',
             '重庆',
             '台州',
             '南京',
             '滨州',
             '贵阳',
             '无锡',
             '本溪',
             '克拉玛依',
             '渭南',
             '马鞍山',
             '宝鸡',
             '焦作',
             '句容',
             '北京',
             '徐州',
             '衡水',
             '包头',
             '绵阳',
             '乌鲁木齐',
             '枣庄',
             '杭州',
             '淄博',
             '鞍山',
             '溧阳',
             '库尔勒',
             '安阳',
             '开封',
             '济南',
             '德阳',
             '温州',
             '九江',
             '邯郸',
             '临安',
             '兰州',
             '沧州',
             '临沂',
             '南充',
             '天津',
             '富阳',
             '泰安',
             '诸暨',
             '郑州',
             '哈尔滨',
             '聊城',
             '芜湖',
             '唐山',
             '平顶山',
             '邢台',
             '德州',
             '济宁',
             '荆州',
             '宜昌',
             '义乌',
             '丽水',
             '洛阳',
             '秦皇岛',
             '株洲',
             '石家庄',
             '莱芜',
             '常德',
             '保定',
             '湘潭',
             '金华',
             '岳阳',
             '长沙',
             '衢州',
             '廊坊',
             '菏泽',
             '合肥',
             '武汉',
             '大庆']
    add = dict(zip(cites, [0] * len(cites)))

    ans = {}

    for x in add.keys():
        for y in records1:
            if x in y['address']:
                add[x] += y['address__count']
    for i in records2:
        records4.append([i['salary'], i['salary__count']])

    for x in add.keys():
        for y in records:
            if x in y.address:
                ans.setdefault(x, [0, 0])
                ans[x][0] += y.salary
                ans[x][1] += 1

    params['json_address'] = json.dumps(list(add.items()))
    params['json_salary'] = json.dumps(records4)
    params['avg_salary'] = json.dumps(ans)
    return render(request, 'html/job_chart.html', params)


@is_login
@cache_page(60 * 15)
def shop_table(request):
    params = {'user_name': request.user,
              'shop_records': None}
    costs = cache.get('costs')
    if not costs:
        costs = models.Cost.objects.filter(user_id=request.user)
        cache.set('costs', costs, 60 * 15)

    all_shopping = costs.filter(consume_type__in=shopping)
    all_income = costs.filter(consume_type__in=income)

    params['shop_records'] = all_shopping
    params['income_records'] = all_income
    # cache.set('costs', costs, 60 * 15)

    return render(request, 'html/shop_table.html', params)


@is_login
@cache_page(60 * 15)
def shop_chart(request):
    params = {'user_name': request.user,
              }
    costs = cache.get('costs')
    if not costs:
        costs = models.Cost.objects.filter(user_id=request.user)
        cache.set('costs', costs, 60 * 15)
    shopping_records = []
    income_records = []
    all_shopping = costs.filter(consume_type__in=shopping)
    all_income = costs.filter(consume_type__in=income)
    if costs:
        params['all_costs'] = round(all_shopping.aggregate(Sum('price'))['price__sum'], 2)
        params['income'] = round(all_income.aggregate(Sum('price'))['price__sum'], 2)
        for item in shopping:
            try:
                mount = round(all_shopping.filter(consume_type=item).aggregate(Sum('price'))['price__sum'], 2)
                shopping_records.append([item, mount])
            except:
                shopping_records.append([item, 0])
        params['shopping_records'] = json.dumps(shopping_records)

        for item in income:
            try:
                mount = round(all_shopping.filter(consume_type=item).aggregate(Sum('price'))['price__sum'], 2)
                income_records.append([item, mount])
            except:
                income_records.append([item, 0])
        params['income_records'] = json.dumps(shopping_records)

    # today = now().date()
    today = datetime.date(2017, 5, 5)

    weekends_index = today.weekday()

    week_cost = [0] * 7
    week_income = [0] * 7
    count = 0
    for i in range(weekends_index, -1, -1):
        start = today - timedelta(days=i)
        end = start + timedelta(days=1)
        today_costs = all_shopping.filter(shopping_time__range=(start, end))
        # print(today_costs)
        today_income = all_income.filter(shopping_time__range=(start, end))

        if today_costs:
            try:
                week_cost[count] = round(today_costs.aggregate(Sum('price'))['price__sum'], 2)
            except:
                pass
        if today_income:
            try:
                week_income[count] = round(today_income.aggregate(Sum('price'))['price__sum'], 2)
            except:
                pass
        count += 1

    params['today_costs'] = week_cost[weekends_index]
    params['today_income'] = week_income[weekends_index]
    params['week_income'] = json.dumps(week_income)
    params['week_cost'] = json.dumps(week_cost)

    return render(request, 'html/shop_chart.html', params)


@is_login
@cache_page(60 * 15)
def reading_table(request):
    params = {'user_name': request.user,
              }
    records = models.Borrow_records.objects.filter(user_id=request.user).order_by('time').reverse()
    params['borrow'] = records
    rank1 = models.Borrow_records.objects.values('user_id').annotate(Count('user_id')).order_by(
        'user_id__count').reverse()[0:10]
    rank2 = models.Borrow_records.objects.values('book_id').annotate(Count('book_id')).order_by(
        'book_id__count').reverse()[0:10]
    params['rank_reader'] = rank1
    params['rank_books'] = rank2
    return render(request, 'html/book_table.html', params)


@is_login
@cache_page(60 * 15)
def reading_chart(request):
    params = {'user_name': request.user,
              }
    records = models.Borrow_records.objects.filter(user_id=request.user)
    # today = now().date()
    today = datetime.date(2012, 10, 13)

    weekends_index = today.weekday()

    count = 0

    week_borrow = [0] * 7
    for i in range(weekends_index, -1, -1):
        start = today - timedelta(days=i)
        end = start + timedelta(days=1)
        today_read = records.filter(time__range=(start, end))
        if today_read:
            try:
                week_borrow[count] = today_read.aggregate(Count('book_id'))['book_id__count']
            except:
                pass
        count += 1

    params['week_read'] = json.dumps(week_borrow)
    return render(request, 'html/book_chart.html', params)


@is_login
def basic_table(request):
    params = {'user_name': request.user,
              'income': 0,
              'today_income': 0,
              'all_costs': 0,
              'today_costs': 0,
              'shopping_records': None,
              'week_cost': None,
              'week_income': None, }
    return render(request, 'html/message_table.html', params)


@is_login
def complete_table(request):
    params = {'user_name': request.user,
              'income': 0,
              'today_income': 0,
              'all_costs': 0,
              'today_costs': 0,
              'shopping_records': None,
              'week_cost': None,
              'week_income': None, }
    return render(request, 'html/table_complete.html', params)


@is_login
def line_chart(request):
    params = {'user_name': request.user,
              'income': 0,
              'today_income': 0,
              'all_costs': 0,
              'today_costs': 0,
              'shopping_records': None,
              'week_cost': None,
              'week_income': None, }
    return render(request, 'html/chart_line.html', params)


@is_login
def columnar_chart(request):
    params = {'user_name': request.user,
              'income': 0,
              'today_income': 0,
              'all_costs': 0,
              'today_costs': 0,
              'shopping_records': None,
              'week_cost': None,
              'week_income': None, }
    return render(request, 'html/chart_columnar.html', params)


@is_login
def pie_chart(request):
    params = {'user_name': request.user,
              'income': 0,
              'today_income': 0,
              'all_costs': 0,
              'today_costs': 0,
              'shopping_records': None,
              'week_cost': None,
              'week_income': None, }
    return render(request, 'html/message_chart.html', params)


def write_DB(request):  # 写入数据库
    '''
    with open('static/StudentData/学生成绩.csv', 'r') as file:
        records = file.readlines()
        count = 0
        for i in records:
            if count == 0:
                count += 1
                continue
            user_id, year, semester, course_id, score = i.split(',')
            Scores_record = models.Scores(user_id=user_id,
                                          year=year,
                                          semester=semester,
                                          course_id=course_id,
                                          score=int(score))
            count += 1
            Scores_record.save()
    '''

    # with open('static/StudentData/奖学金数据.csv', 'r') as file:
    #     records = file.readlines()
    #     count = 0
    #     for i in records:
    #         if count == 0:
    #             count += 1
    #             continue
    #         user_id, Level = i.split(',')
    #         rank = {'x912': 11, 'z052': 10, 'x616': 9, 'y663': 8, 'z512': 7, 'x492': 6, 'y524': 6, 'y076': 5, 'z918': 4,
    #                 'z735': 3, 'y786': 2, 'x986': 1}
    #         Schoolarship_record = models.Schoolarship(user_id=user_id,
    #                                                   level=rank[Level[:-1]])
    #         print(count)
    #         count += 1
    #         Schoolarship_record.save()


    # with open('static/StudentData/借阅记录.csv', 'r') as file:
    #     records = file.readlines()
    #     count = 0
    #     for i in records:
    #         if count == 0:
    #             count += 1
    #             continue
    #         user_id, book_id, time = i.split(',')
    #         time = time[:-1]  # b-05-10 #
    #         year = {'a': 2012, 'b': 2013, 'c': 2014, 'd': 2015, 'e': 2016}
    #         time = datetime.date(year[time[0]], int(time[2:4]), int(time[5:7]))
    #         print(count)
    #         Borrow_record = models.Borrow_records(user_id=user_id,
    #                                               book_id=book_id,
    #                                               time=time)
    #         count += 1
    #         Borrow_record.save()

    # with open('static/StudentData/就业信息.csv', 'rb') as file:
    #     records = file.readlines()
    #     count = 0
    #     for i in records:
    #         if count == 0:
    #             count += 1
    #             continue
    #         user_id, address, salary = i.decode('utf-8').split(',')
    #         print(count)
    #         try:
    #             salary = ord(salary[0].upper()) * 1000 + int(salary[1:-1])
    #         except:
    #             salary = None
    #         Job_record = models.Job(user_id=user_id,
    #                                 address=address,
    #                                 salary=salary)
    #         count += 1
    #         Job_record.save()


    # with open('static/StudentData/论坛发帖频率.csv', 'rb') as file:
    #     records = file.readlines()
    #     count = 0
    #     columns = None
    #     year = {'a': 2012, 'b': 2013, 'c': 2014, 'd': 2015, 'e': 2016}
    #     for i in records:
    #         if count == 0:
    #             columns = i.decode('utf-8').split(',')
    #             count += 1
    #             continue
    #         line = i.decode('utf-8').split(',')
    #         print(count)
    #         user_id = line[0]
    #         for i in range(1, len(line)):
    #             mount = int(line[i])
    #             time = datetime.date(year[columns[i][0]], int(columns[i][2:4]), int(columns[i][5:7]))
    #
    #             print(user_id, mount, time)
    #
    #             Messages_record = models.Messages(user_id=user_id,
    #                                               time=time,
    #                                               mount=mount)
    #             Messages_record.save()
    #         count += 1

    # with open('static/StudentData/消费记录.csv', 'rb') as file:
    #     records = file.readlines()
    #     count = 0
    #     year = {'a': 2012, 'b': 2013, 'c': 2014, 'd': 2015, 'e': 2016, 'f': 2017}
    #     for i in records:
    #         if count == 0:
    #             count += 1
    #             continue
    #         user_id, consume_type, consume_address, shopping_time, price = i.decode('utf-8').split(',')
    #         print(count)
    #         try:
    #             shopping_time = timezone.datetime(year[shopping_time[0]], int(shopping_time[1:3]),
    #                                               int(shopping_time[4:6]),
    #                                               int(shopping_time[7:9]), int(shopping_time[10:12]),
    #                                               int(shopping_time[13:15]))
    #             shopping_time = timezone.make_aware(shopping_time, timezone.get_current_timezone())
    #             Cost_record = models.Cost(user_id=user_id,
    #                                       consume_type=consume_type,
    #                                       consume_address=consume_address,
    #                                       shopping_time=shopping_time,
    #                                       price=float(price))
    #             Cost_record.save()
    #         except:
    #             pass
    #         count += 1

    # with open('static/StudentData/dfNAstat.csv', 'rb') as file:
    #     records = file.readlines()
    #     count = 0
    #     year = {'a': 2012, 'b': 2013, 'c': 2014, 'd': 2015, 'e': 2016, 'f': 2017}
    #     for i in records:
    #         if count == 0:
    #             count += 1
    #             continue
    #         user_id = i.decode('utf-8').split(',')[0]
    #         print(count)
    #         try:
    #             Id_record = models.Students(user_id=user_id)
    #             Id_record.save()
    #         except:
    #             pass
    #         count += 1

    records = models.Students.objects.values('user_id')
    for i in records:
        User.objects.create_user(username=i['user_id'], password='123')

    return redirect('/')
