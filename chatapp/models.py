from django.db import models
from datetime import datetime, date
# Create your models here.


class Chatboard(models.Model):
    cbusername = models.CharField(max_length=100)
    cbadminname = models.CharField(max_length=100)
    cbmessage = models.TextField()
    cbmsgbyuser = models.BooleanField(default=True)
    cbmsgbyadmin = models.BooleanField(default=False)
    cbtime = models.TimeField(auto_now=False, auto_now_add=True, blank=True)
    cbdatetime = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
