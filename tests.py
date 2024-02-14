import unittest
from unittest.mock import patch, MagicMock
import jwt
from jwt_validator import validate_jwt  


from datetime import datetime, timedelta
import time

future_timestamp = datetime.now() + timedelta(hours=1)  
exp = int(time.mktime(future_timestamp.timetuple()))
class TestJWTValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
   
        with open('keys/public_key.pem', 'r') as f:
            cls.public_key = f.read()
        with open('keys/private_key.pem', 'r') as f:
            cls.private_key = f.read()
            
            
    def generate_jwt(self, payload, headers=None):
        
        return jwt.encode(payload, self.__class__.private_key, algorithm="RS256", headers=headers)

    
    @patch('requests.get')
    def test_validate_jwt_valid(self, mock_get):

        mock_get.return_value = MagicMock(status_code=200, text=self.__class__.public_key)
        valid_payload = {
            "sub": "1234567890",
            "name": "John Doe",
            "iat": int(time.time()),
            "exp": exp, 
        }
        valid_headers = {"x5u": "https://example.com/cert.pem"}
        token = self.generate_jwt(valid_payload, valid_headers)
        print("----------",token,"-------------")
        is_valid, error = validate_jwt(token)
        self.assertTrue(is_valid, msg=f"JWT should be valid. Error: {error}")

   
        self.assertIsNone(error)

    @patch('requests.get')
    def test_validate_jwt_expired(self, mock_get):
 
        mock_get.return_value = MagicMock(status_code=200, text=self.__class__.public_key)
        expired_payload = {
            "sub": "1234567890",
            "name": "John Doe",
            "iat": 1516239022,
            "exp": 1516239022,  
        }
        expired_headers = {"x5u": "https://example.com/cert.pem"}
        token = self.generate_jwt(expired_payload, expired_headers)
        
        is_valid, error = validate_jwt(token)
        self.assertFalse(is_valid)
        self.assertIn("expired", error)


if __name__ == '__main__':
    unittest.main()
