from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import json
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import qrcode
# from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import datetime
import uuid

DB = 'plot_data.sqlite3'

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def index(request):
    """
    """

    day1 = datetime.date.today()    # 今日を取得(時間は含まず)
    day2 = day1 + datetime.timedelta(days=1)  # 1日加算

    str_day1 = day1.strftime("%Y-%m-%d")
    str_day2 = day2.strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cmd = "select * from sagyo_log where dt>='{}' and dt<'{}' ".format(
        str_day1, str_day2)
    # print('---------')
    # print(cmd)
    # print('---------')
    cur.execute(cmd)
    lst = cur.fetchall()

    data_x = []
    data_y = []
    for row in lst:
        print(row)
        data_x.append(row[3])
        data_y.append(row[4])

    cur.close()
    conn.close()

    # data_x=['2019-04-18 16:00:00','2019-04-18 16:00:10','2019-04-18 16:00:13','2019-04-18 16:00:20',]
    # data_y=[1,0,1,0,]

    title = '({}) - ({})'.format(str_day1, str_day2)
    context = {'title': title,
               'data_x': data_x,
               'data_y': data_y}

    return render(request, 'app/index.html', context)


def data_input(request):
    """
    """

    context = {}

    return render(request, 'app/data_input.html', context)


@csrf_exempt
def api_01(request):
    """
    JSON返すAPI
    """

    method = request.method
    # print('メソッド={}'.format(method))

    if request.method == 'GET':
        keyword1 = request.GET['keyword1']
        dt = request.GET['date']
        dictData = {}
        dictData['データ'] = '送信されたキーワードは「{}」です'.format(keyword1)
        dictData['date'] = '送信された時刻は「{}」です'.format(dt)

        json_str = json.dumps(dictData, ensure_ascii=False, indent=2,)
        status = 200
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    elif request.method == 'POST':
        keyword1 = request.POST['keyword1']
        keyword2 = request.POST['keyword2']

        insert_date(keyword2, keyword1)

        dictData = {}
        dictData['データ'] = '送信されたキーワードは「{}+{}」です'.format(keyword1, keyword2)

        json_str = json.dumps(dictData, ensure_ascii=False, indent=2,)
        status = 200
        return HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)


def insert_date(dt, status):
    """
    """

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    sql = "insert into sagyo_log('user_id','sagyo','dt','status') values (?,?,?,?)"
    # dt1=datetime.datetime.now()

    lstData = ['hoge', 'foo', dt, status]
    cur.execute(sql, lstData)
    conn.commit()

    cur.close()
    conn.close()


def qr_code(request):
    """
    """

    # url="|{0}://{1}|".format(request.scheme, request.get_host())
    # print(url)

    # url=HttpRequestRedirect(reverse('app1.views.first'))
    # print(url)

    # keywordがgetで与えられたとき(辞書のkeyが存在したら)
    if 'url' in request.GET:
        url = request.GET['url']

    else:
        url = None

    if url != None:
        img = qrcode.make(url)
    else:
        img = qrcode.make('http://www.yahoo.co.jp')
    # print(type(img))
    # print(img.size)
    # <class 'qrcode.image.pil.PilImage'>
    # (290, 290)

    u4 = str(uuid.uuid4())

    # today = datetime.datetime.now()  # 現在の日時を取得
    # img_file = today.strftime("%Y%m%d_%H%M%S")+'.png'  # datetimeのフォーマット
    img_file = u4+'.png'  # datetimeのフォーマット

    img.save('app/static/app/img/' + img_file)

    context = {'img_file': img_file}

    return render(request, 'app/qr_code.html', context)
