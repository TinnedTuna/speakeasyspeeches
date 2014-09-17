import os
import unittest
import tempfile

import speakeasy 
from speakeasy.database.models import init_db, User, db_session
from speakeasy import bcrypt

class PagesTest(unittest.TestCase):
    
    admin_created = False
    def setUp(self):
        self.db_handle, speakeasy.app.config['DATABASE'] = tempfile.mkstemp()
        speakeasy.app.config['TESTING'] = True
        self.app = speakeasy.app.test_client()
        init_db()

    def tearDown(self):
        os.close(self.db_handle)
        os.unlink(speakeasy.app.config['DATABASE'])

    def _login(self, username=None, password=None):
        if username is None:
            real_username = 'admin'
            if not self.admin_created:
                self._create_admin()
        else:
            real_username = username

        if username is None:
            real_password = 'admin_pass'
        else:
            real_password = password 

        res = self.app.post('/authenticate', data=dict(
            username=real_username,
            password=real_password))
        assert res
        print "Login had result: ", res
        return res
    
    def _create_admin(self):
        assert not self.admin_created
        admin_user = User()
        admin_user.username = "admin"
        admin_user.display_name = "Administrator"
        admin_user.password = bcrypt.generate_password_hash("admin_pass")
        db_session.add(admin_user)
        self.admin_Created=True

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

    def test_authenticated_view_create_page(self):
        self._login()
        res = self.app.get('/page/create', follow_redirects=True)
        assert res
        print res.status_code
        assert res.status_code == 200

if __name__ == "__main__":
    unittest.main()
