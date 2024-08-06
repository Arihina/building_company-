import json
import unittest

import requests


class EmployeeTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/employees'

    def test_get_employee(self):
        employee_id = 23
        url = f'{self.BASE_URL}/{employee_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('employee', response_data)
        employee = response_data['employee']
        self.assertIn('full_name', employee)
        self.assertIn('post', employee)
        self.assertIn('phone_number', employee)
        self.assertIn('email', employee)

    def test_get_employees(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_employees(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "New test employee",
            "post": "Сиc Админ",
            "phone_number": "0987654321",
            "email": "new_employee@mail.ru"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_employee(self):
        employee_id = 23
        url = f'{self.BASE_URL}/{employee_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "No test employee",
            "post": "Менеджер",
            "phone_number": "1234567890",
            "email": "test@mail.ru"
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_del_employees(self):
        employee_id = 27
        url = f'{self.BASE_URL}/{employee_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
