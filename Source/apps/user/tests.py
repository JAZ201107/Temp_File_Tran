from django.test import TestCase, SimpleTestCase, Client
from django.urls import resolve, reverse
from apps.user import views


# Create your tests here.
class testView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_user_IoT(self):
        res = self.client.get(reverse('user_IoT'))

        self.assertEqual(res.status_code, 302)

    def test_view_user_upload(self):
        res = self.client.get(reverse('user_upload'))

        self.assertEqual(res.status_code, 302)
