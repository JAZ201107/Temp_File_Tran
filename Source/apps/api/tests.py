from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from apps.api import models, views
import json


# Create your tests here.

class testURLReverse(SimpleTestCase):
    def test_reverse_registeruser(self):
        """ Test for user_IoT revers"""
        url = reverse("registeruser")
        self.assertEqual("/api/registeruser/", url)
        self.assertEqual(resolve(url).func.view_class, views.user_views.UserRegistration)

    def test_reverse_loginuser(self):
        """ Test for user_profile revers"""
        url = reverse("loginuser")
        self.assertEqual("/api/loginuser/", url)
        self.assertEqual(resolve(url).func.view_class, views.account_views.LoginView)


class testUserModels(TestCase):
    def setUp(self):
        models.User.objects.create(email="A123@gmail.com", is_admin=False, is_staff=False,
                                   is_active=True)
        models.User.objects.create(email="B123@gmail.com", is_admin=False, is_staff=False,
                                   is_active=True)

    def test_user_info_GET(self):
        user = models.User.objects.get(email="A123@gmail.com")
        self.assertEqual('A123@gmail.com', user.email)

    def test_user_all_GET(self):
        all_users = models.User.objects.all()
        self.assertEqual(2, len(all_users))


class testUserInfoModels(TestCase):
    def setUp(self):
        models.UserProfileModel.objects.create(
            user_email="123@gmail.com",
            user_name="uowA",
            user_phone_number="1111",
        )
        models.UserProfileModel.objects.create(
            user_email="456@gmail.com",
            user_name="uowB",
            user_phone_number="2222",
        )

    def test_user_profile_get(self):
        user = models.UserProfileModel.objects.get(user_email="123@gmail.com")
        self.assertEqual("123@gmail.com", user.user_email)
        self.assertEqual("uowA", user.user_name)
        self.assertEqual("1111", user.user_phone_number)

    def test_user_profile_post(self):
        user = models.UserProfileModel.objects.get(user_email="123@gmail.com")
        user.user_name = "uowA_Update"
        user.save()
        user = models.UserProfileModel.objects.get(user_email="123@gmail.com")
        self.assertEqual("uowA_Update", user.user_name)

    def test_user_delete(self):
        user = models.UserProfileModel.objects.get(user_email="123@gmail.com")
        user.delete()
        users = models.UserProfileModel.objects.all()
        self.assertEqual(1, len(users))


class testRESTAPIs(TestCase):
    def setUp(self):
        self.client = APIClient()
        models.UserProfileModel.objects.create(
            user_email="123@gmail.com",
            user_name="uowA",
            user_phone_number="1111",
        )
        models.UserProfileModel.objects.create(
            user_email="456@gmail.com",
            user_name="uowB",
            user_phone_number="2222",
        )

    def test_user_info_get(self):
        res = self.client.get("/api/users/info?user_email_h=123@gmail.com")
        self.assertEqual(res.status_code, 200)
        self.assertJSONEqual(
            json.dumps({'user_name': 'uowA',
                        'user_email': '123@gmail.com',
                        'user_address': None,
                        'user_phone_number': '1111'})
            , res.data)

    def test_user_info_update(self):
        res = self.client.put("/api/users/info", data={
            'user_name': 'uowA_update',
            'user_email': '123@gmail.com',
            'user_address': "This is My Address",
            'user_phone_number': '3333'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual("uowA_update", res.data['user_name'])
