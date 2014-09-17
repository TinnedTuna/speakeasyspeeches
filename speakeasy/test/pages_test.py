import os
import unittest
import tempfile

import speakeasy
from speakeasy.database.models import init_db 

class PagesTest(unittest.TestCase):
    
    def setUp(self):
        self.db_handle, speakeasy.app.config['DATABASE'] = tempfile.mkstemp()
        speakeasy.app.config['TESTING'] = True
        self.app = speakeasy.app.test_client()
        init_db()

    def tearDown(self):
        os.close(self.db_handle)
        os.unlink(speakeasy.app.config['DATABASE'])

    def test_get_index(self):
        res = self.app.get('/', follow_redirects=True)
        assert res
        assert res.status_code == 200

    def test_get_non_existant_page(self):
        res = self.app.get('/page/4096', follow_redirects=True);
        assert res
        assert res.status_code == 404

    def test_unauthenticated_attempt_create_page(self):
        res = self.app.post('/page/create', follow_redirects=True,
                data = dict(
                    title = 'test',
                    content= 'test content'))
        assert res
        assert res.status_code == 401

    def test_unauthenticated_view_create_page(self):
        res = self.app.get('/page/create', follow_redirects=True)
        assert res
        assert res.status_code == 401

    def test_unauthenticated_view_edit_page(self):
        res = self.app.get('/page/edit/1', follow_redirects=True)
        assert res
        assert res.status_code == 401

    def test_unauthenticated_view_edit_nonexistent_page(self):
        res = self.app.get('/page/edit/4096', follow_redirects=True)
        assert res
        assert res.status_code == 401

if __name__ == "__main__":
    unittest.main()
