import json
import unittest

import requests


class ClientTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/consists'

    def test_get_consist(self):
        consist_id = 1
        url = f'{self.BASE_URL}/{consist_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('consist', response_data)
        consist = response_data['consist']
        self.assertIn('product_id', consist)
        self.assertIn('order_amount', consist)
        self.assertIn('account_number', consist)
        self.assertIn('data', consist)

    def test_get_consists(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_consist(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            'product_id': 12,
            'order_amount': 15000.0,
            'account_number': '40529075171039588888',
            'data': '2024-09-09 16:00:00'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_consist(self):
        client_id = 23
        url = f'{self.BASE_URL}/{client_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'data': '2024-09-09 16:30:00'
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_no_found(self):
        client_id = 500
        url = f'{self.BASE_URL}/{client_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

    def test_del_consist(self):
        consist_id = 23
        url = f'{self.BASE_URL}/{consist_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
