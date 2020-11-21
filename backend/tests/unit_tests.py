import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from ..api import app
from ..database.modelss import setup_db, Bookmark, Category


admin_token = os.environ['AUTH0_ADMIN_TOKEN']
user_token = os.environ['AUTH0_USER_TOKEN']


class BookmarkTestCase(unittest.TestCase):
    """
        This class represents the bookmark test case
    """

    def setUp(self):
        """
            Define test variables and initialize app
        """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookmark_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Inserting a bookmark
        self.new_bookmark = {
            "title": "Personal Site",
            "url": "https://rayan.dev"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """
            Executed after reach test
        """
        pass

    def test_get_bookmarks(self):
        """
            Test for getting list of bookmarks
        """

        res = self.client().get('/bookmarks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['bookmarks']))

    def test_404_get_bookmarks_beyond_valid_pagination(self):
        """
            Test for 404 getting bookmarks beyond valid pagination
        """

        res = self.client().get('/bookmarks?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_user_get_categories(self):
        """
            Test for getting list of categories by user
        """

        self.headers.update({'Authorization': 'Bearer ' + str(user_token)})

        res = self.client().get('/categories', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_404_get_categories_beyond_valid_pagination(self):
        """
            Test for 404 getting bookmarks beyond valid pagination
        """

        res = self.client().get('/categories?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_user_create_bookmark(self):
        """
            Test for creating a bookmark by a user
        """

        self.headers.update({'Authorization': 'Bearer ' + str(user_token)})
        res = self.client().post(
            '/bookmarks', json=self.new_bookmark, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['bookmarks'])

    def test_405_create_nonexistent_bookmark(self):
        """
            Test for 405 creating a nonexistent bookmark
        """

        res = self.client().post(
            '/bookmarks/300', json=self.new_bookmark)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_update_bookmark(self):
        """
            Test for updating a bookmark by admin
        """

        # ! Increment bookmark_id before execution
        bookmark_id = 5

        self.headers.update({'Authorization': 'Bearer ' + str(admin_token)})

        res = self.client().patch('/bookmarks/' + str(bookmark_id),
                                  json=self.new_bookmark, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['bookmark'])

    def test_404_update_nonexistent_bookmark(self):
        """
            Test for updating a nonexistent bookmark
        """

        res = self.client().patch(
            '/bookmarks/1500', json=self.new_bookmark)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_delete_bookmark(self):
        """
            Test for deleting a bookmark by admin
        """

        # ! Increment bookmark_id before execution
        bookmark_id = 9

        self.headers.update({'Authorization': 'Bearer ' + str(user_token)})

        res = self.client().delete('/bookmarks/' + str(bookmark_id),
                                   headers=self.headers)
        data = json.loads(res.data)

        bookmark = Bookmark.query.filter(
            Bookmark.id == bookmark_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], bookmark_id)

    def test_404_delete_nonexistent_bookmark(self):
        """
            Test for 404 deleting a nonexistent bookmark
        """

        res = self.client().delete('/bookmarks/3000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
