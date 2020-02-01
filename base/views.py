from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Message
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')


def message(request):
    if request.method == 'POST':
        name = request.POST["name"]
        subject = request.POST["subject"]
        emailid = request.POST["emailid"]
        usrmessage = request.POST["usrmessage"]

        msg = Message.objects.create(name=name, subject=subject, emailid=emailid, usrmessage=usrmessage)
        msg.save()
        messages.info(request, "Message Send Successfully")
        return redirect(reverse('index'))
