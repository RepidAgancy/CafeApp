from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from product import models, utils
from accounts.models import User, STOREKEEPER
from product.utils import create_test_image


class ProductTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='behruz', password='behruz1234', type=STOREKEEPER
        )
        self.category = models.CategoryProduct.objects.create(
            name='osh', image='test.jpg'
        )

    def test_storekeeper_can_create_product(self):
        self.client.login(username='behruz', password='behruz1234')
        data = {
            'category': self.category.id,
            'product_name': 'Palov',
            'price': 15.000,
            'image': create_test_image(),
        }
        response = self.client.post(f'/api/v1/product/product/create/', data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Product is successfully created')

    def test_product_create_failed(self):
        self.client.login(username='behruz', password='behruz1234')
        data = {
            'category': '3',
            'product_name': 'Palov',
            'price': 15.000,
            'image': create_test_image(),
        }
        response = self.client.post(f'/api/v1/product/product/create/', data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], [ErrorDetail(string='Category does not exist', code='invalid')])




class ProductCategoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='behruz', password='behruz1234', type=STOREKEEPER
        )
        self.category = models.CategoryProduct.objects.create(
            name='osh', image='test.jpg'
        )

    def test_get_product_category_list(self):
        self.client.login(username='behruz', password='behruz1234')

        response = self.client.get(f'/api/v1/product/product-category/list/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data[0])
        self.assertIn('name_uz', response.data[0])
        self.assertIn('name_ru', response.data[0])
        self.assertIn('name_en', response.data[0])
        self.assertIn('image', response.data[0])
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name_uz'], 'osh')
        self.assertEqual(response.data[0]['name_ru'], None)
        self.assertEqual(response.data[0]['name_en'], None)
        self.assertEqual(response.data[0]['image'], 'http://testserver/media/test.jpg')

