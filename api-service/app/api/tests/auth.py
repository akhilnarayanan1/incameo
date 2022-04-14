from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from api.models import AllVerifyOrForgotToken

User = get_user_model()
fake = Faker()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.email = fake.email()
        self.password = fake.password()
        User.objects.create_user(email=self.email, password=self.password)

    def test_signup(self):
        """
        Test Signup API and check if token created 
        as well as password encrypted
        """
        data = {'email': fake.email(), 'password': fake.password()}
        response = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(check_password(data['password'], User.objects.get(email=data['email']).password))

    def test_signup_with_existing_account(self):
        """
        Test Signup API with duplicate account, 
        first one should create, second should throw 400
        """
        data = {'email': fake.email(), 'password': fake.password()}
        response1 = self.client.post('/api/signup/', data, format='json')
        response2 = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_for_token(self):
        """
        Test Signup API having new verification token
        """
        data = {'email': fake.email(), 'password': fake.password()}
        response = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AllVerifyOrForgotToken.objects.filter(user=User.objects.get(email=data['email']), 
            token_type='verify').count(), 1)

    def test_create_verification_token(self):
        """
        Test verification token API should throw 401
        if user not loggedin, 201 if user recognized
        400 again if token is already present
        """
        data = {'user': self.email}
        response1 = self.client.post('/api/account/verify/', data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=User.objects.get(email=data['user']))
        response2 = self.client.post('/api/account/verify/', data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        response3 = self.client.post('/api/account/verify/', data, format='json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_forgot_token(self):
        """
        Test forgot token API should throw 400
        if user not present(no login needed), 201 if user recognized
        400 again if token is already present
        """
        data1 = {'user': fake.email()}
        data2 = {'user': self.email}
        response1 = self.client.post('/api/account/forgot/', data1, format='json')
        response2 = self.client.post('/api/account/forgot/', data2, format='json')
        response3 = self.client.post('/api/account/forgot/', data2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_token(self):
        """
        Test verification and forgot token API should throw 404
        if token not present, 200 if token recognized
        """
        data = {'email': fake.email(), 'password': fake.password()}
        response1 = self.client.post('/api/signup/', data, format='json')
        response2 = self.client.post('/api/account/forgot/', {'user': data['email']}, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        token_obj1 = AllVerifyOrForgotToken.objects.filter(user=User.objects.get(email=data['email']), token_type='verify').first()
        token_obj2 = AllVerifyOrForgotToken.objects.filter(user=User.objects.get(email=data['email']), token_type='forgot').first()
        
        response3 = self.client.get(f'/api/account/verify/{token_obj1.token}/', format='json')
        response4 = self.client.get(f'/api/account/verify/{fake.pystr(min_chars=32, max_chars=32)}/', format='json')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.status_code, status.HTTP_404_NOT_FOUND)
        
        response5 = self.client.get(f'/api/account/forgot/{token_obj2.token}/', format='json')
        response6 = self.client.get(f'/api/account/forgot/{fake.pystr(min_chars=32, max_chars=32)}/', format='json')
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(response6.status_code, status.HTTP_404_NOT_FOUND)
