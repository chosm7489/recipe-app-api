from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**param):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    #Test the users API (public)

    def setUp(self):
        self.client = APIClient()

    def test_cresate_valid_user_success(self):
        #Test creating user with valid payload is test_create_user_with_email_successful
        payload = {
            'email':'test@londonappdev.com',
            'password':'testpass',
            'name':'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertEqual(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        #Test creatlings user that already exists fails
        payload = {'email':'test@londonappdev.com','password':'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        #Test that the password must be more than 5 characters
        payload = {'email':'test@londonappdev.com','password':'pw'}
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)
