import json
import unittest

import requests


class ManagerTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/managers'

    def test_get_profile(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('manager', response_data)
        manager = response_data['manager']
        self.assertIn('phone_number', manager)
        self.assertIn('full_name', manager)
        self.assertIn('email', manager)

    def test_get_drivers(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}/drivers'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)
        if response_data:
            driver = response_data[0]
            self.assertIn('id', driver)
            self.assertIn('phone_number', driver)
            self.assertIn('full_name', driver)
            self.assertIn('car_type', driver)

    def test_get_orders(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}/orders'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)
        if response_data:
            order = response_data[0]
            self.assertIn('id', order)
            self.assertIn('client_name', order)
            self.assertIn('driver_name', order)
            self.assertIn('product_name', order)
            self.assertIn('product_volume', order)
            self.assertIn('data', order)
            self.assertIn('deliver_address', order)
            self.assertIn('warehouse_address', order)
            self.assertIn('order_amount', order)

    def test_post_order(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}/orders'
        headers = {'Content-Type': 'application/json'}
        data = {
            "client_name": None,
            "product_name": None,
            "driver_name": None,
            "client_id": 1,
            "product_id": 1,
            "driver_id": 1,
            "warehouse_id": 1,
            "delivery_address": "test",
            "data": "2024-09-09 12:00:00",
            "order_amount": 1200,
            "prepayment": 100,
            "account_number": "123456789",
            "product_volume": 12
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_forbidden_put_order(self):
        manager_id = 1
        order_id = 1
        url = f'{self.BASE_URL}/{manager_id}/orders'
        headers = {'Content-Type': 'application/json'}
        data = {
            'id': order_id,
            'deliver_address': 'new test order'
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 403)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_put_order(self):
        manager_id = 3
        order_id = 19
        url = f'{self.BASE_URL}/{manager_id}/orders'
        headers = {'Content-Type': 'application/json'}
        data = {
            'id': order_id,
            'deliver_address': 'new test order'
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_get_clients(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}/clients'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)
        if response_data:
            client = response_data[0]
            self.assertIn('phone_number', client)
            self.assertIn('full_name', client)
            self.assertIn('organization_name', client)

    def test_post_client(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}/clients'
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "test name",
            "phone_number": "12345678910",
            "organization_name": None
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_get_completes_orders(self):
        manager_id = 1
        url = f'{self.BASE_URL}/{manager_id}/orders/completes'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)
        if response_data:
            order = response_data[0]
            self.assertIn('id', order)
            self.assertIn('client_name', order)
            self.assertIn('driver_name', order)
            self.assertIn('product_name', order)
            self.assertIn('product_volume', order)
            self.assertIn('data', order)
            self.assertIn('deliver_address', order)
            self.assertIn('warehouse_address', order)
            self.assertIn('order_amount', order)


if __name__ == '__main__':
    unittest.main()
