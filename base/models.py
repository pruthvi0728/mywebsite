from django.db import models

# Create your models here.


class Message(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    emailid = models.CharField(max_length=100)
    usrmessage = models.TextField()
