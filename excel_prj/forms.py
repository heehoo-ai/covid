# 文件上传表单
from django import forms


class FileForm(forms.Form):
    file_name = forms.FileField(label=u"数据文件")