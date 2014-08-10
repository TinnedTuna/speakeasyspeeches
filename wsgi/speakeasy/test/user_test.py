import os
import unittest
import tempfile
from speakeasy import app

class UserTests(unittest.TestCase):
    
    def setUp(self):
        self.db_handle, speakeasy.app.config['DATABASE'] = tempfile.mkstemp()
        speakeasy.app.config['TESTING'] = True
        self.app = speakeasy.app.test_client()
        speakeasy.init_db()

    def tearDown(self):
        os.close(self.db_handle)
        os.unlink(speakeasy.app.config['DATABASE'])

if __name__ == "__main__":
    unittest.main()
