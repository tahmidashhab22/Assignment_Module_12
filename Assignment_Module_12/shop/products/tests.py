from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

URL = '/api/products/'
VALID = {"name": "Notebook", "description": "A notebook with 100 pages.",
         "price": "120.00", "stock": 25}


class ProductAPITests(APITestCase):
    def setUp(self):
        user = User.objects.create_user('testuser', password='pass12345')
        self.token = Token.objects.create(user=user)

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_empty_list_without_token(self):
        r = self.client.get(URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['results'], [])
        self.assertEqual(r.data['count'], 0)

    def test_create_with_token(self):
        self.auth()
        r = self.client.post(URL, VALID, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertIn('id', r.data)
        self.assertEqual(r.data['name'], 'Notebook')

    def test_create_without_token_denied(self):
        r = self.client.post(URL, VALID, format='json')
        self.assertEqual(r.status_code, 401)

    def test_invalid_token_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token wrong')
        self.assertEqual(self.client.post(URL, VALID, format='json').status_code, 401)

    def test_empty_name(self):
        self.auth()
        r = self.client.post(URL, {**VALID, "name": ""}, format='json')
        self.assertEqual(r.status_code, 400)
        self.assertIn('name', r.data)

    def test_whitespace_name(self):
        self.auth()
        r = self.client.post(URL, {**VALID, "name": "   "}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_price_zero_and_negative(self):
        self.auth()
        for price in ("0", "-5.00"):
            r = self.client.post(URL, {**VALID, "price": price}, format='json')
            self.assertEqual(r.status_code, 400)
            self.assertIn('price', r.data)

    def test_negative_stock(self):
        self.auth()
        r = self.client.post(URL, {**VALID, "stock": -1}, format='json')
        self.assertEqual(r.status_code, 400)
        self.assertIn('stock', r.data)

    def test_non_integer_stock(self):
        self.auth()
        r = self.client.post(URL, {**VALID, "stock": 2.5}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_page_two_shows_sixth_product(self):
        self.auth()
        for i in range(1, 7):
            self.client.post(URL, {**VALID, "name": f"Item {i}"}, format='json')
        self.client.credentials()
        r = self.client.get(URL + '?page=2')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data['results']), 1)
        self.assertEqual(r.data['results'][0]['name'], 'Item 6')

    def test_ordered_by_id(self):
        self.auth()
        for i in range(3):
            self.client.post(URL, {**VALID, "name": f"P{i}"}, format='json')
        ids = [p['id'] for p in self.client.get(URL).data['results']]
        self.assertEqual(ids, sorted(ids))
