from django.shortcuts import render
from .models import Message
# Create your views here.


def index(request):
    return render(request, 'index.html')


def message(request):
    name = request.POST["name"]
    subject = request.POST["subject"]
    emailid = request.POST["emailid"]
    usrmessage = request.POST["usrmessage"]
    return render(request, 'UsrMessage.html', {'name': name, 'subject': subject, 'emailid': emailid, 'usrmessage': usrmessage})
