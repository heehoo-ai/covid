from django.db import models

# Create your models here.
class AllInfo(models.Model):
    confirm = models.IntegerField(verbose_name='确诊')
    dead = models.IntegerField(verbose_name="死亡")
    heal = models.IntegerField(verbose_name="治愈")
    date = models.DateTimeField(verbose_name="创建日期")

    class Meta:
        verbose_name = "今日总体数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Covid-19: {}>'.format(self.name)


class MxInfo(models.Model):
    province = models.CharField(max_length=50, verbose_name="省")
    city = models.CharField(max_length=50, verbose_name="市")
    confirm = models.IntegerField(verbose_name='确诊')
    suspect = models.IntegerField(verbose_name="死亡")
    cured = models.IntegerField(verbose_name="治愈")
    time_info = models.DateTimeField(verbose_name="更新时间")
    date = models.DateTimeField(auto_now_add=True,verbose_name="创建日期", null=True)

    class Meta:
        verbose_name = "各省信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Covid-19: {}>'.format(self.name)


