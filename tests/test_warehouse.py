import json
import unittest

import requests


class WarehouseTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/warehouses'

    def test_get_warehouse(self):
        warehouse_id = 2
        url = f'{self.BASE_URL}/{warehouse_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('warehouse', response_data)
        product = response_data['warehouse']
        self.assertIn('address', product)
        self.assertIn('product_id', product)
        self.assertIn('quantity', product)

    def test_get_warehouses(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_warehouse(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            "address": "test address",
            "product_id": 5,
            "quantity": 1000
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_warehouse(self):
        warehouse_id = 23
        url = f'{self.BASE_URL}/{warehouse_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'quantity': 500
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_del_warehouse(self):
        warehouse_id = 23
        url = f'{self.BASE_URL}/{warehouse_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_no_found(self):
        warehouse_id = 500
        url = f'{self.BASE_URL}/{warehouse_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
