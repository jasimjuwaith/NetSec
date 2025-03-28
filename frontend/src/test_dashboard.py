import unittest
import requests

class TestDashboardAPI(unittest.TestCase):
    def test_api_call(self):
        response = requests.get('http://localhost:3000/api/real-time-data')  # Update endpoint
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()
