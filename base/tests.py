from django.test import TestCase, Client
from django.urls import reverse, resolve
from .views import index, message
from .models import Message
# Create your tests here.


class TestUrls(TestCase):

    def test_index_resolve(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_message_resolve(self):
        url = reverse('message')
        print(resolve(url))
        self.assertEquals(resolve(url).func, message)


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.message_url = reverse('message')

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_message_POST(self):
        self.msgcred = {'name': 'Test', 'subject': 'TestSub', 'emailid': 'Test@test.com', 'usrmessage': 'TestMessage'}
        response = self.client.post(self.message_url, self.msgcred, follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class TestModel(TestCase):

    def setUp(self):
        self.msg = Message.objects.create(name='Test', subject='TestSub', emailid='Test@test.com', usrmessage='TestMessage')
    
    def test_message_model(self):
        self.assertEquals(self.msg.emailid, 'Test@test.com')
