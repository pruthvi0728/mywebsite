from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .views import login, register, logout, chatmain, selectusr
from .models import Chatboard
# Create your tests here.


class TestUrls(TestCase):
    def test_login_resolve(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_resolve(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_register_resolve(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_chatmain_resolve(self):
        url = reverse('chatmain')
        self.assertEquals(resolve(url).func, chatmain)

    def test_selectusr_resolve(self):
        url = reverse('selectusr')
        self.assertEquals(resolve(url).func, selectusr)


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Test001', email='Test@test.com', password='Test987')
        self.cred = {'username': 'Test001', 'password': 'Test987'}
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        self.chatmain_url = reverse('chatmain')
        self.selectusr_url = reverse('selectusr')

    # done
    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    # done
    def test_logout_GET(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # done
    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    # done
    def test_chatmain_GET(self):
        self.client.login(username='Test001', password='Test987')
        session = self.client.session
        session['user_loggedin'] = True
        session.save()
        response = self.client.get(self.chatmain_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatmain.html')

    # done
    def test_selectusr_GET(self):
        self.client.login(username='Test001', password='Test987')
        session = self.client.session
        session['user_loggedin'] = True
        session['admin_loggedin'] = True
        session.save()
        response = self.client.get(self.selectusr_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'selectusr.html')

    # done
    def test_login_POST(self):
        response = self.client.post(self.login_url, self.cred, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatmain.html')

    # done
    def test_register_POST(self):
        self.rcred = {'firstname': 'Test', 'lastname': 'Test001', 'username': 'Test002', 'emailid': 'test@test.com',
                     'password1': 'test123', 'password2': 'test123'}
        response = self.client.post(self.register_url, self.rcred, follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    # done
    def test_chatmain_POST(self):
        self.client.login(username='Test001', password='Test987')
        self.ccred = {'msg': 'Hellotest', 'username': 'Test001'}
        session = self.client.session
        session['user_loggedin'] = True
        session.save()
        response = self.client.post(self.chatmain_url, self.ccred, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatmain.html')

    # done
    def test_selectusr_POST(self):
        self.client.login(username='Test001', password='Test987')
        self.scred = {'radiobtn': 'Test001'}
        session = self.client.session
        session['user_loggedin'] = True
        session.save()
        response = self.client.post(self.selectusr_url, self.scred, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatmain.html')
