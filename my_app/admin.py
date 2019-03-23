from django.contrib import admin
from .models import Anli
# Register your models here.

@admin.register(Anli)
class AnliAdmin(admin.ModelAdmin):
    list_display = ("id","anli_time","city","title","result","point")
    ordering = ("id",)