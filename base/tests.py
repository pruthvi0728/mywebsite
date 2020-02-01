from django.test import TestCase
from django.urls import reverse, resolve
from .views import index, message
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
