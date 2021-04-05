from django.db import models
from account.models import CustomUser
import datetime
from datetime import date
from django.utils import timezone


class File(models.Model):
    title  = models.CharField(max_length=70)
    description = models.CharField(max_length=300,blank=True,null=True)
    file_field = models.FileField(upload_to='files')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    add_date = models.DateField(editable=False,blank=True,null=True)
    expr_date = models.DateField(editable=False,blank=True,null=True)

    def save(self,*args, **kwargs):
        self.add_date = date.today()
        self.expr_date = self.add_date + datetime.timedelta(days=7)
        
        super(File,self).save(*args, **kwargs)
    




class Permission(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    file_f =models.ForeignKey(File,on_delete=models.CASCADE)
    comment = models.BooleanField(default=False)

    def __str__(self):
        return "%s-%s"%(self.file_f.title,self.user.username)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    file = models.ForeignKey(File,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True,null=True)

