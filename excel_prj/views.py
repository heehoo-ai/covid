import os
import datetime
import pandas as pd
from pandas import to_datetime
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from xlrd import xldate_as_datetime

from covid import settings
from excel_prj import models
import xlrd


# 将excel数据写入mysql
from excel_prj.models import Sensor


def wrdb(filename):
    # 打开上传 excel 表格
    readboot = xlrd.open_workbook(settings.UPLOAD_ROOT + "/" + filename)
    # 获取所有sheet工作表名称
    sheetnames = readboot.sheet_names()
    print(len(sheetnames))
    for sheetname in sheetnames:
        print(sheetname)
        sheet = readboot.sheet_by_name(sheetname)
        # 获取excel的行和列
        nrows = sheet.nrows
        ncols = sheet.ncols
        sensor_name = sheetname
        id = models.Sensor.objects.get(name=sensor_name).id
        # print(ncols,nrows,name)
        # ObservationDate = xldate_as_datetime(row[0], 0).strftime('%Y%m%d'),
        # 控制数据库事务交易
        with transaction.atomic():
            for i in range(2, nrows):
                row = sheet.row_values(i)
                models.SensorData.objects.create(
                    ObservationDate=xldate_as_datetime(row[0], 0),
                    sensor_id=id,
                    R1=float(row[1]),
                    R2=float(row[2]),
                    F1=float(row[3]),
                    F2=float(row[4]),
                )


def tablelist(request, sensor_id=None):
    sensors = Sensor.objects.filter(isShow=Sensor.SHOW)
    if sensor_id:
        q = models.SensorData.objects.filter(sensor_id=sensor_id).values('sensor__name', 'ObservationDate', 'R1', 'R2', 'F1', 'F2')
        df = pd.DataFrame.from_records(q)
        datalist = df.values.tolist()
    else:
        datalist = models.SensorData.objects.all().values('sensor__name', 'ObservationDate', 'R1', 'R2', 'F1', 'F2')
    return render(request, "dataList.html", {'datalist': datalist, 'sensors': sensors, 'sensor_id':sensor_id})


def echarts(request, sensor_id=None):
    date_list = []
    r1_list = []
    r2_list = []
    sensors = Sensor.objects.filter(isShow=Sensor.SHOW)

    if sensor_id:
        q = models.SensorData.objects.filter(sensor_id=sensor_id).values('ObservationDate', 'R1', 'R2')
        df = pd.DataFrame.from_records(q)
        d = df['ObservationDate'].apply(lambda x: datetime.datetime.strftime(x, "%Y-%m-%d"))
        date_list = d.values.tolist()
        print(date_list)
        r1_list = df.R1.values.tolist()
        r2_list = df['R2'].values.tolist()
    else:
        datalist = models.SensorData.objects.filter(sensor_id=1)
        for data in datalist:
            time_info = datetime.datetime.strftime(data.ObservationDate, "%Y-%m-%d")
            date_list.append(time_info)
            r1_list.append(data.R1)
            r2_list.append(data.R2)

    print(date_list)

    context = {
        'date': date_list,
        'r1': r1_list,
        'r2': r2_list,
        'sensors': sensors,

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
    # return HttpResponse('上传并导入成功')
    return HttpResponseRedirect(reverse('table'))




