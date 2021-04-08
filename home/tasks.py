from os import name
from celery import shared_task
from home.models import *
import datetime 

@shared_task(name='deleting_files')
def delete_file_after_7_days():
    files = File.objects.all()
    for file in files:
        if file.expr_date == datetime.date.today():
            file.delete()
        continue


