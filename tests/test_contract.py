import json
import unittest

import requests


class ContractTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/contracts'

    def test_get_contract(self):
        contract_id = 24
        url = f'{self.BASE_URL}/{contract_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('contract', response_data)
        contract = response_data['contract']
        self.assertIn('contract_consist_id', contract)
        self.assertIn('client_id', contract)
        self.assertIn('employee_id', contract)

    def test_get_contracts(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_contract(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            'contract_consist_id': 24,
            'client_id': 1,
            'employee_id': 1
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_contract(self):
        contract_id = 24
        url = f'{self.BASE_URL}/{contract_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'client_id': 5
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_no_found(self):
        contract_id = 500
        url = f'{self.BASE_URL}/{contract_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

    def test_del_contract(self):
        contract_id = 24
        url = f'{self.BASE_URL}/{contract_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
