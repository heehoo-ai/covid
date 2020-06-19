from django.db import models

# Create your models here.




class Sensor(models.Model):
    SHOW = 1
    HIDE = 0
    STATUS_ITEMS = (
        (SHOW, '显示'),
        (HIDE, '隐藏'),
    )
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name="测点编号")
    isShow = models.BooleanField(default=SHOW, choices=STATUS_ITEMS, verbose_name="是否显示")

    class Meta:
        verbose_name = "测点"
        verbose_name_plural = "测点"

    def __str__(self):
        return self.name


# 成果文件
class SensorData(models.Model):
    sensor = models.ForeignKey(to=Sensor, null=True, blank=True, verbose_name="测点", on_delete=models.DO_NOTHING)
    ObservationDate = models.DateTimeField(verbose_name="创建时间", null=True, blank=True)
    R1 = models.FloatField(verbose_name="原始测值1", null=True, blank=True)
    R2 = models.FloatField(verbose_name="原始测值2", null=True, blank=True)
    F1 = models.FloatField(verbose_name="计算结果1", null=True, blank=True)
    F2 = models.FloatField(verbose_name="计算结果2", null=True, blank=True)
    Note = models.CharField(max_length=20, verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = "人工观测数据"
        verbose_name_plural = verbose_name

