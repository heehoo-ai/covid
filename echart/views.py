import datetime

from django.shortcuts import render

# Create your views here.
from .models import AllInfo


def index(request):
    all_info = AllInfo.objects.all()
    date_list = []
    confirm_list = []
    dead_list = []
    heal_list = []
    for info in all_info:
        time_info = datetime.datetime.strftime(info.date, "%Y-%m-%d")
        date_list.append(time_info)
        confirm_list.append(info.confirm)
        dead_list.append(info.dead)
        heal_list.append(info.heal)
    print(date_list)
    context = {
        'confirm': confirm_list,
        'dead': dead_list,
        'heal': heal_list,
        'date': date_list,
    }
    return render(request, template_name="index.html", context=context)