import os
import datetime
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from xlrd import xldate_as_datetime

from covid import settings
from covid.settings import MEDIA_ROOT
from excel_prj import models
from excel_prj.forms import FileForm
from excel_prj.models import Sensor
import xlrd


# 将excel数据写入mysql
def wrdb(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    sheet = readboot.sheet_by_index(0)
    #获取excel的行和列
    nrows = sheet.nrows
    ncols = sheet.ncols
    print(ncols,nrows)
    # ObservationDate = xldate_as_datetime(row[0], 0).strftime('%Y%m%d'),
    # 控制数据库事务交易
    with transaction.atomic():
        for i in range(2, nrows):
            row = sheet.row_values(i)
            models.SensorData.objects.create(
                ObservationDate=xldate_as_datetime(row[0],0),
                R1=float(row[1]),
                R2=float(row[2]),
                F1=float(row[3]),
                F2=float(row[4]),
            )


def tablelist(request):
    datalist = models.SensorData.objects.all().values('ObservationDate', 'R1', 'R2', 'F1', 'F2')
    print(datalist)
    return render(request, "dataList.html", {'datalist': datalist})


def echarts(request):
    datalist = models.SensorData.objects.all()
    date_list = []
    r1_list = []
    r2_list = []

    for data in datalist:
        time_info = datetime.datetime.strftime(data.ObservationDate, "%Y-%m-%d")
        date_list.append(time_info)
        r1_list.append(data.R1)
        r2_list.append(data.R2)

    context = {
        'date': date_list,
        'r1': r1_list,
        'r2': r2_list,

    }

    return render(request, 'echarts.html', context=context)


@csrf_exempt
def upload(request):

    file = request.FILES.get('datafile')
    # 创建upload文件夹
    if not os.path.exists(settings.UPLOAD_ROOT):
        os.makedirs(settings.UPLOAD_ROOT)
    try:
        if file is None:
            # return HttpResponse('请选择要上传的文件')
            return render(request, 'upload.html')
        # 循环二进制写入
        with open(settings.UPLOAD_ROOT + "/" + file.name, 'wb') as f:
            for i in file.readlines():
                f.write(i)

    except Exception as e:
        return HttpResponse(e)
    wrdb(file.name)
    return HttpResponse('上传并导入成功')



