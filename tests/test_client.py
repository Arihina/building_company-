import json
import unittest

import requests


class ClientTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/clients'

    def test_get_client(self):
        client_id = 1
        url = f'{self.BASE_URL}/{client_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('client', response_data)
        client = response_data['client']
        self.assertIn('full_name', client)
        self.assertIn('phone_number', client)
        self.assertIn('organization_name', client)

    def test_get_clients(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_client(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "New test client",
            "phone_number": "0987654321",
            "organization_name": "test org 2"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_client(self):
        client_id = 27
        url = f'{self.BASE_URL}/{client_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "No test client"
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

    def test_del_client(self):
        client_id = 27
        url = f'{self.BASE_URL}/{client_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
