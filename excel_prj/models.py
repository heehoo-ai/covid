from django.db import models

# Create your models here.


# 原始文件
class Sensor(models.Model):
    sensor_id = models.CharField(max_length=20, verbose_name="仪器编号")
    file_name = models.FileField(upload_to='upload/', verbose_name=u"文件名称")

    # 不注释会报错
    # def __str__(self):
    #     return self.file_name

    # 定义表名称
    class Meta:
        verbose_name = "原始数据文件"
        verbose_name_plural = "原始数据文件"


# 成果文件
class SensorData(models.Model):
    # sensor = models.ForeignKey(Sensor, verbose_name="仪器编号", on_delete=models.CASCADE)
    ObservationDate = models.DateTimeField(verbose_name="创建时间")
    R1 = models.FloatField(verbose_name="原始测值1")
    R2 = models.FloatField(verbose_name="原始测值2")
    F1 = models.FloatField(verbose_name="计算结果1")
    F2 = models.FloatField(verbose_name="计算结果2")
    Note = models.CharField(max_length=20, verbose_name="备注")

    class Meta:
        verbose_name = "人工观测数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Sensor