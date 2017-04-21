"""
These unit tests will upload a test file,a test folder and a test contact,
Perform api operations on them,
And them remove them from your account.
"""
from mega import Mega
import unittest
import random
import os

mega = Mega()
# anonymous login
m = mega.login()
# normal login
#m = mega.login(email, password)

FIND_RESP = None
TEST_CONTACT = 'test@mega.co.nz'
TEST_PUBLIC_URL = 'https://mega.nz/#!1iYHkDTL!rIivzxhmNxHpMzeuua0qPE4_zu9YWz8nhePDUJD6rok'
TEST_FILE = os.path.basename(__file__)
TEST_FOLDER = 'mega.py_testfolder_{0}'.format(random.random())


class TestMega(unittest.TestCase):

    def test_mega(self):
        self.assertIsInstance(mega, Mega)

    def test_get_user(self):
        resp = m.get_user()
        self.assertIsInstance(resp, dict)

    def test_get_quota(self):
        resp = m.get_quota()
        self.assertIsInstance(int(resp), int)

    def test_get_storage_space(self):
        resp = m.get_storage_space(mega=True)
        self.assertIsInstance(resp, dict)

    def test_get_files(self):
        files = m.get_files()
        self.assertIsInstance(files, dict)

    def test_get_link(self):
        file = m.find(TEST_FILE)
        if file:
            link = m.get_link(file)
            self.assertIsInstance(link, str)

    def test_import_public_url(self):
        resp = m.import_public_url(TEST_PUBLIC_URL)
        file_handle = m.get_id_from_obj(resp)
        resp = m.destroy(file_handle)
        self.assertIsInstance(resp, int)

    def test_create_folder(self):
        resp = m.create_folder(TEST_FOLDER)
        self.assertIsInstance(resp, dict)

    def test_rename(self):
        file = m.find(TEST_FOLDER)
        if file:
            resp = m.rename(file, TEST_FOLDER)
            self.assertIsInstance(resp, int)

    def test_delete_folder(self):
        folder_node = m.find(TEST_FOLDER)[0]
        resp = m.delete(folder_node)
        self.assertIsInstance(resp, int)

    def test_delete(self):
        file = m.find(TEST_FILE)
        if file:
            resp = m.delete(file[0])
            self.assertIsInstance(resp, int)

    def test_destroy(self):
        file = m.find(TEST_FILE)
        if file:
            resp = m.destroy(file[0])
            self.assertIsInstance(resp, int)

    def test_empty_trash(self):
        #resp None if already empty, else int
        resp = m.empty_trash()
        if resp is not None:
            self.assertIsInstance(resp, int)

    def test_add_contact(self):
        resp = m.add_contact(TEST_CONTACT)
        self.assertIsInstance(resp, int)

    def test_remove_contact(self):
        resp = m.remove_contact(TEST_CONTACT)
        self.assertIsInstance(resp, int)


class LoginTests(unittest.TestCase):

    mega = None
    email = None
    password = None

    def setUp(self):
        self.mega = Mega()
        self.email = os.getenv('MEGA_USER')
        self.password = os.getenv('MEGA_PASSWORD')

    def test_login__user(self):
        self.assertIsNone(self.mega.sid)
        self.mega.login('guigarfr@gmail.com', 'redpoints0')
        self.assertIsNotNone(self.mega.sid)

    def test_login__anonymous(self):
        self.assertIsNone(self.mega.sid)
        self.mega.login()
        self.assertIsNotNone(self.mega.sid)


if __name__ == '__main__':
    unittest.main()
