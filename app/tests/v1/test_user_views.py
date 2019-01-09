"""This will test the user auth endpoint"""
import json
import unittest
from app.api import APP

class TestUserviewEndpoints(unittest.TestCase):
    """class that handles USERVIEW endpont"""
    
    def setUp(self):
        """This code will be executed before each test"""
        # Propagate exceptions to the test class
        APP.testing = True
        # Creating a test client
        self.app = APP.test_client()
        # Data that we are posting
        self.data = {
            "username": "user_1",
            "email": "email@email.com",
            "password": "password"
        }

    def test_landing(self):
        """Test if the user registration is functions efficiently"""
        # This self.app is the test client
        response = self.app.post('/auth/signin',
                                 data = json.dumps(self.data),
                                 content_type="application/json")

        # Now lets need load the response
        result = json.loads(response.data)

        self.assertEqual(result["status"], "ok")

        self.assertEqual(result["username"], "user_1")
        self.assertEqual(result["email"], "email@email.com")
        self.assertEqual(response.status_code, 201)
        
        # Pass Status code
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()