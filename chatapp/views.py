from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from .models import Chatboard
from django.contrib import messages
from .msgenc import msgdecode, msgencode
from datetime import datetime
# Create your views here.

selectusername = None
key = 'QfTjWnZr4u7x!A%C*F-JaNdRgUkXp2s5v8y/B?E(G+KbPeShVmYq3t6w9z$C&F)J@McQfTjWnZr4u7x!A%D*G-KaPdRgUkXp2s5v'


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
                return redirect('selectusr')
            request.session['user_loggedin'] = True
            return redirect('chatmain')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        if request.session.has_key('user_loggedin'):
            return redirect('chatmain')
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
        if request.session.has_key('user_loggedin'):
            return redirect('chatmain')
        else:
            return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def chatmain(request):
    global selectusername
    if request.method == 'POST':
        cbmsg = request.POST['msg']
        cbadminname = 'Admin_Pruthvi'
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
            return redirect('chatmain')
        else:
            msg = Chatboard.objects.create(cbusername=cbusername, cbadminname=cbadminname, cbmessage=cbmsg)
            msg.save()
            return redirect('chatmain')
    else:
        if request.session.has_key('user_loggedin'):
            msgs = Chatboard.objects.order_by('cbdatetime')
            for msg in msgs:
                msg.cbmessage = msgdecode(msg.cbmessage, key)
            return render(request, 'chatmain.html', {'msgs': msgs, 'selectusrname': selectusername, 'key': key})
        else:
            return redirect('login')


@login_required
def selectusr(request):
    global selectusername
    if request.method == 'POST':
        selectusername = request.POST['radiobtn']
        return redirect('chatmain')
    else:
        if request.session.has_key('admin_loggedin'):
            msgs = Chatboard.objects.all()
            usrlist = []
            for un in msgs:
                if un.cbusername not in usrlist:
                    usrlist.append(un.cbusername)
            return render(request, 'selectusr.html', {'msg': msgs, 'usrlist': usrlist})
        else:
            return redirect('login')
