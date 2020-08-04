import requests
import time
import unittest

host = 'http://localhost:8080/api/users'


class TestGetApi(unittest.TestCase):
    """TestCases with GET method"""

    def test_size_of_page(self):
        """Size of page should be equal params['size']"""
        params = {'size': 10}
        r_get = requests.get(host, params=params)
        self.assertEqual(r_get.status_code, 200)
        self.assertEqual(len(r_get.json()['_embedded']['users']), 10)

    def test_uncreated_user(self):
        """Response to get uncreated user should be 404"""
        r_get = requests.get(f'{host}/100')
        self.assertEqual(r_get.status_code, 404)


class TestPostApi(unittest.TestCase):
    """TestCases with POST method"""

    def tearDown(self):
        """Deleting created user"""
        r_delete = requests.delete(f'{host}/{self.new_user_id}')
        self.assertEqual(r_delete.status_code, 204)

    def test_day_of_birth_match_format(self):
        """Format of 'dayOfBirth' field should be 'YYYY-mm-dd'"""
        payload = {"firstName": "Ivan",
                   "lastName": "Ivanov",
                   "dayOfBirth": "15-01-2000",
                   "email": "ivanov@test.com"}
        r_post = requests.post(host, json=payload)
        self.assertEqual(r_post.status_code, 400)
        payload.update({"dayOfBirth": "2000-01-15"})
        r_post = requests.post(host, json=payload)
        self.assertEqual(r_post.status_code, 201)
        self.new_user_id = r_post.json()['id']
        r_get = requests.get(f'{host}/{self.new_user_id}')
        self.assertEqual(r_get.status_code, 200)
        self.assertTrue(bool(time.strptime(r_get.json()['dayOfBirth'], '%Y-%m-%d')))

    def test_day_of_birth_earlier_current_date(self):
        """'dayOfBirth' field's date should be earlier than current date"""
        payload = {"firstName": "Ivan",
                   "lastName": "Ivanov",
                   "dayOfBirth": time.strftime("%Y-%m-%d", time.gmtime()),  # Today's day
                   "email": "ivanov@test.com"}
        r_post = requests.post(host, json=payload)
        self.assertEqual(r_post.status_code, 400)
        payload.update({"dayOfBirth": "2000-01-15"})
        r_post = requests.post(host, json=payload)
        self.assertEqual(r_post.status_code, 201)
        self.new_user_id = r_post.json()['id']
        r_get = requests.get(f'{host}/{self.new_user_id}')
        self.assertEqual(r_get.status_code, 200)
        self.assertLess(r_get.json()['dayOfBirth'], time.strftime("%Y-%m-%d", time.gmtime()))


class TestPutUsersApi(unittest.TestCase):
    """TestCases with PUT method"""

    def setUp(self):
        """Creating new user"""
        self.payload = {"firstName": "Ivan",
                        "lastName": "Ivanov",
                        "dayOfBirth": "2000-01-15",
                        "email": "ivanov@test.com"}
        r_post = requests.post(host, json=self.payload)
        self.assertEqual(r_post.status_code, 201)
        self.new_user_id = r_post.json()['id']

    def tearDown(self):
        """Deleting created user"""
        r_delete = requests.delete(f'{host}/{self.new_user_id}')
        self.assertEqual(r_delete.status_code, 204)

    def test_updating_resource(self):
        """Resource should be updated"""
        new_payload = {"firstName": "Alexei",
                       "lastName": "Alexeev",
                       "dayOfBirth": "2002-01-15",
                       "email": "alexeev@test.com"}
        r_put = requests.put(f'{host}/{self.new_user_id}', json=new_payload)
        self.assertEqual(r_put.status_code, 200)
        r_get = requests.get(f'{host}/{self.new_user_id}')
        r_get_json = r_get.json()
        self.assertEqual(
            [r_get_json['firstName'], r_get_json['lastName'], r_get_json['dayOfBirth'], r_get_json['email']],
            [new_payload['firstName'], new_payload['lastName'], new_payload['dayOfBirth'], new_payload['email']])


class TestDeleteApi(unittest.TestCase):
    """TestCases with DELETE method"""

    def setUp(self):
        """Creating new user"""
        self.payload = {"firstName": "Ivan",
                        "lastName": "Ivanov",
                        "dayOfBirth": "2000-01-15",
                        "email": "ivanov@test.com"}
        r_post = requests.post(host, json=self.payload)
        self.assertEqual(r_post.status_code, 201)
        self.new_user_id = r_post.json()['id']

    def test_deleting_created_user(self):
        r_delete = requests.delete(f'{host}/{self.new_user_id}')
        self.assertEqual(r_delete.status_code, 204)
        r_get = requests.get(f'{host}/{self.new_user_id}')
        self.assertEqual(r_get.status_code, 404)


if __name__ == '__main__':
    unittest.main()

