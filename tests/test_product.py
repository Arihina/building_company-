import json
import unittest

import requests


class ProductTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/products'

    def test_get_product(self):
        product_id = 2
        url = f'{self.BASE_URL}/{product_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('product', response_data)
        product = response_data['product']
        self.assertIn('name', product)
        self.assertIn('type', product)
        self.assertIn('unit_type', product)
        self.assertIn('price', product)

    def test_get_products(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_product(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            'name': "New test product",
            'type': "type",
            'unit_type': "unit",
            'price': 12.7
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_product(self):
        product_id = 22
        url = f'{self.BASE_URL}/{product_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'price': 127.3
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_del_product(self):
        product_id = 22
        url = f'{self.BASE_URL}/{product_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_no_found(self):
        product_id = 500
        url = f'{self.BASE_URL}/{product_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
