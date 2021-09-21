from dotenv import dotenv_values
from app import init_app
import unittest
import json


class MyGameListTestCase(unittest.TestCase):
    def setUp(self):
        self.app = init_app()
        self.client = self.app.test_client
        self.user_token = dotenv_values('.env').get('USER_TEST')
        self.manager_token = dotenv_values('.env').get('MANAGER_TEST')

        # set imagelink to self.imagelink because line too long
        # and resulting pylint error variable value too long
        self.imglink = 'https://img2.storyblok.com/fit-in/0x1000/filters:format(webp)/\
            f/110098/1920x1080/b1876da855/productionline.jpeg'

    def tearDown(self):
        pass

    def test_get_gamelist(self):
        """
        Public endpoint /api/gamelists operation get test
        """
        response = self.client().get('http://localhost:8000/api/gamelists')
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/gamelists endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test.get('games'), list)

    def test_get_game_detail(self):
        """
        Public endpoint /api/gamelist/<id> operation get test
        """
        response = self.client().get('http://localhost:8000/api/gamelist/6')
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/gamelist/<id> endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test, object)

    def test_get_vendors(self):
        """
        Public endpoint /api/vendors operation get test
        """
        response = self.client().get('http://localhost:8000/api/vendors')
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/vendors endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test.get('vendors'), list)

    def test_get_vendor_detail(self):
        """
        Public endpoint /api/vendor/<id> operation get test
        """
        response = self.client().get('http://localhost:8000/api/vendor/2')
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/vendor/<id> endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test, object)

    def test_get_my_info(self):
        """
        Authenticated and RBAC Authorized endpoint /api/user/me operation get test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        response = self.client().get('http://localhost:8000/api/user/me', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/user/me endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test, object)

    def test_get_my_game(self):
        """
        Authenticated and RBAC Authorized endpoint /api/user/me/games operation get test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        response = self.client().get('http://localhost:8000/api/user/me/games', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/user/me/games endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test.get('myGames'), list)

    def test_add_my_gamelist(self):
        """
        Authenticated and RBAC Authorized endpoint /api/user/me/games operation add test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        data = {
            "purchased_on": "Tue Sep 21 2021 01:57:57 GMT+0800 (WITA)",
            "game_id": 6,
            "vendor_id": 4
        }

        response = self.client().post('http://localhost:8000/api/user/me/games', headers=headers, json=data)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/user/me/games endpoint (operation::POST)\n ')
        self.assertEqual(status, 201)
        self.assertEqual(test.get('literal_status'), 'saved')
        self.assertIsInstance(test.get('list_id'), int)

    def test_edit_my_gamelist(self):
        """
        Authenticated and RBAC Authorized endpoint /api/user/me/games/<id> operation edit test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        data = {
            "play_status": True
        }

        response = self.client().patch('http://localhost:8000/api/user/me/games/21', headers=headers, json=data)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/user/me/games/<id> endpoint (operation::PATCH)\n ')
        self.assertEqual(status, 200)
        self.assertEqual(test.get('literal_status'), 'updated')
        self.assertIsInstance(test, object)

    def test_delete_my_gamelist(self):
        """
        Authenticated and RBAC Authorized endpoint /api/user/me/games/<id> operation delete test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        response = self.client().delete('http://localhost:8000/api/user/me/games/19', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/user/me/games/<id> endpoint (operation::DELETE)\n ')
        self.assertEqual(status, 200)
        self.assertEqual(test.get('literal_status'), 'deleted')
        self.assertIsInstance(test.get('list_id'), int)

    def test_get_userlist(self):
        """
        Authenticated and RBAC Authorized endpoint /api/users operation get test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        response = self.client().get('http://localhost:8000/api/users', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/users endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test.get('users'), list)

    def test_get_userdetail(self):
        """
        Authenticated and RBAC Authorized endpoint /api/user/<id> operation get test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        response = self.client().get('http://localhost:8000/api/user/61470d6d44672c00694cfd14', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/user/<id> endpoint (operation::GET)\n ')
        self.assertEqual(status, 200)
        self.assertIsInstance(test, object)

    def test_post_new_game(self):
        """
        Authenticated and RBAC Authorized endpoint /api/gamelists operation post test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        data = {
            "name": "Satisfactory 2",
            "price": "20",
            "rating": "5",
            "platform": ["Windows"],
            "genre": ["Simulation", "Open World", "First Person"],
            "cover_link": self.imglink,
            "vendor_id": 4
        }

        response = self.client().post('http://localhost:8000/api/gamelists', headers=headers, json=data)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/gamelists endpoint (operation::POST)\n ')
        self.assertEqual(status, 201)
        self.assertEqual(test.get('literal_status'), 'saved')
        self.assertIsInstance(test.get('content'), object)

    def test_edit_game(self):
        """
        Authenticated and RBAC Authorized endpoint /api/gamelist/<id> operation edit test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        data = {
            "name": "test update",
            "price": "20",
            "rating": "5",
            "platform": ["Windows"],
            "genre": ["Simulation", "Open World", "First Person"],
            "cover_link": self.imglink,
        }

        response = self.client().patch('http://localhost:8000/api/gamelist/12', headers=headers, json=data)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/gamelist/<id> endpoint (operation::PATCH)\n ')
        self.assertEqual(status, 200)
        self.assertEqual(test.get('literal_status'), 'updated')
        self.assertIsInstance(test, object)

    def test_delete_game(self):
        """
        Authenticated and RBAC Authorized endpoint /api/gamelist/<id> operation delete test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        response = self.client().delete('http://localhost:8000/api/gamelist/18', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/gamelist/<id> endpoint (operation::DELETE)\n ')

        self.assertEqual(status, 200)
        self.assertEqual(test.get('literal_status'), 'deleted')
        self.assertIsInstance(test.get('list_id'), int)

    def test_post_new_vendor(self):
        """
        Authenticated and RBAC Authorized endpoint /api/vendors operation post test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        data = {
            "name": "datastudio",
            "developer": "datastudio",
            "distributor": "datastudio",
            "publisher": "datastudio",
            "release_date": "Tue Sep 21 2021 21:00:21 GMT+0800 (WITA)"
        }

        response = self.client().post('http://localhost:8000/api/vendors', headers=headers, json=data)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/vendors endpoint (operation::POST)\n ')
        self.assertEqual(status, 201)
        self.assertEqual(test.get('literal_status'), 'saved')
        self.assertIsInstance(test.get('content'), object)

    def test_edit_vendor(self):
        """
        Authenticated and RBAC Authorized endpoint /api/vendor/<id> operation edit test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        data = {
            "name": "patchdatastudio",
            "developer": "patchdatastudio",
            "distributor": "patchdatastudio",
            "publisher": "patchdatastudio",
            "release_date": "Tue Sep 21 2021 21:00:21 GMT+0800 (WITA)"
        }

        response = self.client().patch('http://localhost:8000/api/vendor/12', headers=headers, json=data)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/vendor/<id> endpoint (operation::PATCH)\n ')
        self.assertEqual(status, 200)
        self.assertEqual(test.get('literal_status'), 'updated')
        self.assertIsInstance(test, object)

    def test_delete_vendor(self):
        """
        Authenticated and RBAC Authorized endpoint /api/vendor/<id> operation delete test
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.manager_token}'
        }

        response = self.client().delete('http://localhost:8000/api/vendor/3', headers=headers)
        status = response.status_code
        test = json.loads(response.data)

        print('\n[*] Testing /api/vendor/<id> endpoint (operation::DELETE)\n ')
        self.assertEqual(status, 200)
        self.assertEqual(test.get('literal_status'), 'deleted')
        self.assertIsInstance(test.get('list_id'), int)

    def test_error_401_test(self):
        """
        Error test code 401 (unauthorized)

        raised when user fail anything related to authorization
        """

        response = self.client().get('http://localhost:8000/api/users')
        status = response.status_code

        print('\n[*] Testing error endpoint 401 (operation::GET)\n ')
        self.assertEqual(status, 401)

    def test_error_403_test(self):
        """
        Error test code 403 (forbidden)

        raised when trying to inserting data with empty body E.g. editing data with empty body
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        # expected body
        # {
        #    "play_status": True
        # }

        response = self.client().patch('http://localhost:8000/api/user/me/games/6', headers=headers, json="")
        status = response.status_code

        print('\n[*] Testing error endpoint 403 (operation::POST)\n ')
        self.assertEqual(status, 403)

    def test_error_404_test(self):
        """
        Error test code 404 (forbidden)

        raised resource id is not founded in database.
        """
        response = self.client().get('http://localhost:8000/api/gamelist/77')
        status = response.status_code

        print('\n[*] Testing error endpoint 404 (operation::GET)\n ')
        self.assertEqual(status, 404)

    def test_error_422_test(self):
        """
        Error test code 422 (Unprocessable Entity)

        raised when trying to create new resource but expected body has unmatch key, or missing a key
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.user_token}'
        }

        data = {
            "game_id": 6,
            "vendor_id": 4
        }

        # expected body key
        # {
        #     "purchased_on": "Tue Sep 21 2021 01:57:57 GMT+0800 (WITA)",
        #     "game_id": 6,
        #     "vendor_id": 4
        # }

        response = self.client().post('http://localhost:8000/api/user/me/games', headers=headers, json=data)
        status = response.status_code

        print('\n[*] Testing /api/user/me/games endpoint (operation::POST)\n ')
        self.assertEqual(status, 422)

    def test_error_500_test(self):
        """
        Error test code 500 (Server Error)

        raised when data exchange between server and Auth0 server have some trouble
        this error included detail error what is wrong in filed ServerError.detail
        """
        pass


if __name__ == '__main__':
    unittest.main()
