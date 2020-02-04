from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from .models import Chatboard
from django.contrib import messages
from .msgenc import msgdecode, msgencode
from django.urls import reverse
from decouple import config
from datetime import datetime
# Create your views here.

selectusername = None
key = config('ENC_KEY')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                request.session['user_loggedin'] = True
                request.session['admin_loggedin'] = True
                request.session.set_expiry(0)
                return redirect(reverse('selectusr'))
            request.session['user_loggedin'] = True
            request.session.set_expiry(0)
            return redirect(reverse('chatmain'))
        else:
            messages.info(request, "Invalid Credentials")
            return redirect(reverse('login'))
    else:
        if request.session.has_key('user_loggedin'):
            return redirect(reverse('chatmain'))
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
            return redirect(reverse('register'))
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username Taken")
            return redirect(reverse('register'))
        elif User.objects.filter(email=emailid).exists():
            messages.info(request, "Already Have Account try login")
            return redirect(reverse('login'))
        else:
            user = User.objects.create_user(username=username, email=emailid, password=password1, first_name=firstname,
                                            last_name=lastname)
            user.save()
            messages.info(request, "Account Created Successfully")
            return redirect(reverse('login'))
    else:
        if request.session.has_key('user_loggedin'):
            return redirect(reverse('chatmain'))
        else:
            return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    try:
        del request.session["user_loggedin"]
        del request.session["admin_loggedin"]
    except KeyError:
        pass
    return redirect(reverse('index'))


@login_required
def chatmain(request):
    global selectusername
    if request.method == 'POST':
        cbmsg = request.POST['msg']
        cbadminname = config('ADMIN_NAME')
        cbusername = request.POST['username']
        cbmsg = msgencode(cbmsg, key)

        if cbusername == cbadminname:
            cbmsgbyuser = 'False'
            cbmsgbyadmin = 'True'
            cbusername = request.POST['selusername']
            selectusername = cbusername
            msg = Chatboard.objects.create(cbusername=cbusername, cbadminname=cbadminname, cbmessage=cbmsg,
                                           cbmsgbyuser=cbmsgbyuser, cbmsgbyadmin=cbmsgbyadmin)
            msg.save()
            return redirect(reverse('chatmain'))
        else:
            msg = Chatboard.objects.create(cbusername=cbusername, cbadminname=cbadminname, cbmessage=cbmsg)
            msg.save()
            return redirect(reverse('chatmain'))
    else:
        if request.session.has_key('user_loggedin'):
            msgs = Chatboard.objects.order_by('cbdatetime')
            for msg in msgs:
                msg.cbmessage = msgdecode(msg.cbmessage, key)
            return render(request, 'chatmain.html', {'msgs': msgs, 'selectusrname': selectusername, 'key': key})
        else:
            return redirect(reverse('login'))


@login_required
def selectusr(request):
    global selectusername
    if request.method == 'POST':
        selectusername = request.POST['radiobtn']
        return redirect(reverse('chatmain'))
    else:
        if request.session.has_key('admin_loggedin'):
            msgs = Chatboard.objects.all()
            usrlist = []
            for un in msgs:
                if un.cbusername not in usrlist:
                    usrlist.append(un.cbusername)
            return render(request, 'selectusr.html', {'msg': msgs, 'usrlist': usrlist})
        else:
            return redirect(reverse('login'))
