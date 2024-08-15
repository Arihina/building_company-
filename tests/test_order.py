import json
import unittest

import requests


class OrdersTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/orders'

    def test_get_order(self):
        order_id = 4
        url = f'{self.BASE_URL}/{order_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('order', response_data)
        order = response_data['order']
        self.assertIn('contract_id', order)
        self.assertIn('warehouse_id', order)
        self.assertIn('delivery_address', order)
        self.assertIn('driver_id', order)
        self.assertIn('prepayment', order)
        self.assertIn('product_volume', order)
        self.assertIn('status', order)

    def test_get_orders(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_order(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            'contract_id': 24,
            'warehouse_id': 1,
            'delivery_address': 'test',
            'driver_id': 3,
            'prepayment': 10000.,
            'product_volume': 15,
            'status': False
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_order(self):
        order_id = 25
        url = f'{self.BASE_URL}/{order_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'delivery_address': 'not test address'
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_no_found(self):
        order_id = 500
        url = f'{self.BASE_URL}/{order_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

    def test_del_order(self):
        order_id = 24
        url = f'{self.BASE_URL}/{order_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
