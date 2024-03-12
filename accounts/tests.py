# accounts/tests.py
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from django.urls import reverse
from .models import CustomUser
from branches.models import *
from django.contrib.auth.hashers import make_password, check_password


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@mahshellsoft.com",
            password=make_password("testpassword"),
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@mahshellsoft.com")
        self.assertFalse(user.check_password("testpassword"))
        self.assertTrue(check_password("testpassword", make_password("testpassword")))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = CustomUser.objects.create_superuser(
            username="adminuser",
            email="adminuser@mahshellsoft.com",
            password=make_password("adminpassword"),
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_non_passenger_user(self):
        client = Client.objects.create(
            name="Jama'a", allowed_branches=5, created_branches=2
        )
        admin = CustomUser.objects.create(
            username="testuser",
            email="testuser@mahshellsoft.com",
            password=make_password("testpassword"),
            role="Admin",
            client=client,
        )

        driver = CustomUser.objects.create(
            username="testdriver",
            email="testdriver@mahshellsoft.com",
            password=make_password("testpassword"),
            role="Driver",
            client=client,
        )

        self.assertEqual(admin.role, "Admin")
        self.assertTrue(admin.client)
        self.assertEqual(admin.client, client)

        self.assertEqual(driver.role, "Driver")
        self.assertNotEqual(driver.role, "Passenger")
        self.assertTrue(driver.client)
        self.assertEqual(driver.client, client)

    def test_create__non_passenger_user_without_client_attribute(self):
        admin = CustomUser.objects.create(
            username="testuser",
            email="testuser@mahshellsoft.com",
            password=make_password("testpassword"),
            role="Admin",
        )

        driver = CustomUser.objects.create(
            username="testdriver",
            email="testdriver@mahshellsoft.com",
            password=make_password("testpassword"),
            role="Driver",
        )

        self.assertEqual(admin.role, "Admin")
        self.assertFalse(admin.client)

        self.assertEqual(driver.role, "Driver")
        self.assertFalse(driver.client)

        self.assertNotEqual(driver.role, "Admin")
        self.assertFalse(driver.client)


class CustomUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="apiuser",
            email="apiuser@mahshellsoft.com",
            password="apipassword",
            role="Admin",
            is_staff=True,
        )

        self.regular_user = CustomUser.objects.create_user(
            username="apiuser-regular",
            email="apiuser.regular@mahshellsoft.com",
            password="apipassword",
            role="Passenger",
        )

        self.user_list_url = reverse("customuser-list")
        self.user_detail_url = reverse("customuser-detail", args=[self.user.id])

        self.admin_create_user_url = reverse("admin-customuser-list")

    def test_list_users(self):
        # Simulate authentication
        self.client.force_authenticate(user=self.user)

        # Print the authentication status directly from the response
        response = self.client.get(self.user_list_url)
        print("Authentication status:", response.wsgi_request.user)
        # print(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_users_regular_user(self):
        # Authenticate as a regular user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse("customuser-list"))

        self.assertEqual(response.status_code, 403)

    def test_retrieve_user(self):
        # Simulate authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_detail_url)

        print("Authentication status:", response.wsgi_request.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "apiuser")

    def test_create_passenger_user_without_auth(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
        }

        response = self.client.post(self.user_list_url, data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("client", response.data)

    def test_create_non_passenger_user_without_client(self):
        user1 = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "role": "ADMIN",
        }

        user2 = {
            "username": "newuseri",
            "email": "newuseri@example.com",
            "password": "newpassword",
            "role": "DRIVER",
            "client": 0,
        }
        self.client.force_authenticate(user=self.user)

        response1 = self.client.post(self.admin_create_user_url, user1)
        response2 = self.client.post(self.admin_create_user_url, user2)

        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)
        self.assertNotIn("client", response1.data)

    def test_create_regular_user_without_auth_and_client(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "role": "PASSENGER",
        }

        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("client", response.data)
