from django.db import models

# Create your models here.

class Anli(models.Model):
    anli_time = models.DateField(verbose_name="事件时间")
    city = models.TextField(verbose_name="城市")
    title = models.TextField(verbose_name="案例名称")
    content = models.TextField(verbose_name="事件经历")
    result = models.TextField(verbose_name="事件结果")
    point = models.TextField(verbose_name="事件特点")

    def __str__(self):
        return self.title
