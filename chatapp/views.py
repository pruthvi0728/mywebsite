from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Chatboard
from django.contrib import messages
# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatmain')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        emailid = request.POST['emailid']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.info(request, "Password mismatch")
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username Taken")
            return redirect('register')
        elif User.objects.filter(email=emailid).exists():
            messages.info(request, "Already Have Account try login")
            return redirect('login')
        else:
            user = User.objects.create_user(username=username, email=emailid, password=password1, first_name=firstname,
                                            last_name=lastname)
            user.save()
            messages.info(request, "Account Created Successfully")
            return redirect('login')
    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def chatmain(request):
    if request.method == 'POST':
        cbmsg = request.POST['msg']
        cbadminname = 'Admin_Pruthvi'
        cbusername = request.POST['username']

        if cbusername == cbadminname:
            cbmsgbyuser = 'False'
            cbmsgbyadmin = 'True'
            cbusername = 'raj07'
            msg = Chatboard.objects.create(cbusername=cbusername, cbadminname=cbadminname, cbmessage=cbmsg,
                                           cbmsgbyuser=cbmsgbyuser,cbmsgbyadmin=cbmsgbyadmin)
            msg.save()
            return redirect('chatmain')
        else:
            msg = Chatboard.objects.create(cbusername=cbusername, cbadminname=cbadminname, cbmessage=cbmsg)
            msg.save()
            return redirect('chatmain')
    else:
        msgs = Chatboard.objects.all()
        return render(request, 'chatmain.html', {'msgs': msgs})
