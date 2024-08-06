import json
import unittest

import requests


class DriverTestCase(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000/drivers'

    def test_get_driver(self):
        driver_id = 4
        url = f'{self.BASE_URL}/{driver_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('driver', response_data)
        driver = response_data['driver']
        self.assertIn('full_name', driver)
        self.assertIn('phone_number', driver)
        self.assertIn('car_type', driver)

    def test_get_drivers(self):
        url = self.BASE_URL

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIsInstance(response_data, list)

    def test_post_driver(self):
        url = self.BASE_URL
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "New test driver",
            "phone_number": "88005553535",
            "car_type": "test car"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'CREATED')

    def test_put_driver(self):
        driver_id = 12
        url = f'{self.BASE_URL}/{driver_id}'
        headers = {'Content-Type': 'application/json'}
        data = {
            "full_name": "No test client"
        }

        response = requests.put(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(response_data['message'], 'UPDATED')

    def test_no_found(self):
        driver_id = 500
        url = f'{self.BASE_URL}/{driver_id}'

        response = requests.get(url)
        self.assertEqual(response.status_code, 404)

    def test_del_driver(self):
        driver_id = 12
        url = f'{self.BASE_URL}/{driver_id}'

        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
