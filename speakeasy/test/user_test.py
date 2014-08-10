import os
import unittest
import tempfile

import speakeasy
from speakeasy.database.models import init_db 

class UserTests(unittest.TestCase):
    
    def setUp(self):
        self.db_handle, speakeasy.app.config['DATABASE'] = tempfile.mkstemp()
        speakeasy.app.config['TESTING'] = True
        self.app = speakeasy.app.test_client()
        init_db()

    def tearDown(self):
        os.close(self.db_handle)
        os.unlink(speakeasy.app.config['DATABASE'])

    def test_create_user(self):
        self.app.get('/')

if __name__ == "__main__":
    unittest.main()
