import unittest
from django.test import Client
from .models import Product
from rest_framework import status, response
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class CheckProductRegisterTest(APITestCase):

    def setUp(self):
        #Create an user
        self.login_username1 = 'Testing-man'
        self.login_password1 = 'hard#p4s$w0rd'
        self.first_user = User.objects.create_user(self.login_username1, self.login_password1)

        #Create another user
        self.login_username2 = 'Another-test-man'
        self.login_password2 = 'another#p4s$w0rd'
        self.another_user = User.objects.create_user(self.login_username2, self.login_password2)

        self.client = APIClient()

    
    def test_register_product(self):
        #Login with first user:
        self.client.force_authenticate(user=self.first_user)

        #Create a 'product' to post
        prod = {'title':'food','description':'this is a description','price':12.34, 'quantity':2}

        #Checking POST
        first_response = self.client.post('/products/', prod)
        self.assertEqual(first_response.status_code, 201)

        self.assertEqual(first_response.data["title"], prod["title"])
        self.assertEqual(first_response.data["description"], prod["description"])
        self.assertEqual(float(first_response.data["price"]), prod["price"])
        self.assertEqual(first_response.data["quantity"], prod["quantity"])

        #Checking GET
        get_response = self.client.get('/products/')
        self.assertEqual(first_response.status_code, 201)
        self.assertEqual( get_response.data[0]["title"], prod["title"])
        self.assertEqual( get_response.data[0]["description"], prod["description"])
        self.assertEqual( float(get_response.data[0]["price"]), prod["price"])
        self.assertEqual( get_response.data[0]["quantity"], prod["quantity"])

        
    def test_products_get_details(self):
        #Login with first user:
        self.client.force_authenticate(user=self.first_user)
        #Create a 'product' to post
        prod = {'title':'food','description':'this is a description','price':12.34, 'quantity':2}
        #Post on first_user
        first_response = self.client.post('/products/', prod)

        #Check get one product
        get_response = self.client.get('/products/' + str(first_response.data['id']) + '/')
        self.assertEqual(first_response.status_code, 201)

        self.assertEqual(get_response.data["title"], prod["title"])
        self.assertEqual(get_response.data["description"], prod["description"])
        self.assertEqual(float(get_response.data["price"]), prod["price"])
        self.assertEqual(get_response.data["quantity"], prod["quantity"])
    
    def test_products_permission(self):
        #Login with first user:
        self.client.force_authenticate(user=self.first_user)
        #Create a 'product' to post
        prod = {'title':'food','description':'this is a description','price':12.34, 'quantity':2}
        #Post on first_user
        first_response = self.client.post('/products/', prod)


        #Changing user to 'anothe_user':
        self.client.force_authenticate(user=self.another_user)

        #Check permissions: Try to delete a product of the first User
        delete_response = self.client.delete('/products/' + str(first_response.data['id']) + '/')
        self.assertNotEqual(delete_response.status_code, 204)

        #Back to first user
        self.client.force_authenticate(user=self.first_user)
        delete_response = self.client.delete('/products/' + str(first_response.data['id']) + '/')
        self.assertEqual(delete_response.status_code, 204)


