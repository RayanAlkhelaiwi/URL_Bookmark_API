import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from backend.api import create_app
from backend.database.models import setup_db, Bookmark, Category


admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhjM3p6enpBZS13OUZuazJ0UWFWdSJ9.eyJpc3MiOiJodHRwczovL3JheWFuLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDUzMzIwMzA4NjQ2ODkzNTQwMjYiLCJhdWQiOlsiYm9va21hcmsiLCJodHRwczovL3JheWFuLWRldi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA0NzczMzU4LCJleHAiOjE2MDQ4NTk3NTgsImF6cCI6Ikp3aGJrVDJMQ3M2NmwzbDNZaDhROFBKNEhGdjd4bmhiIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpib29rbWFya3MiLCJnZXQ6Y2F0ZWdvcmllcyIsInBhdGNoOmJvb2ttYXJrcyIsInBvc3Q6Ym9va21hcmtzIl19.vy2OMmSoJXYUKP4mBkXXzCavTqm53HMpDqWgr5hC03OkdQMoK2Lgs6g6giYSjcV35B_imjQ6Qz1cPJejN00hdk_8R5D9SbeCXPy6Qjbdel8iVne0I2BxYpQwWNxCdVvTkde8BB2OCxVB8D25eZ1ipHFgDliL74JlkBM95w0cFR6jqslEdCstyQ-Uga7waUul6Cl4qWZ8FnwIJZ9OMaOeYa1fsW0y0-72z95TDaUVAqu48ziWm9YXhFhCeFAGz1Dv1OntBj1pb-34M8IgMz98V0MnUQ2Wxsg2I8cQLQu32G4E75qjeTTqSNLvj82zSpn38YT358wxWn7sdbjPLCa6Cg'
user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhjM3p6enpBZS13OUZuazJ0UWFWdSJ9.eyJpc3MiOiJodHRwczovL3JheWFuLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDM1MzY0OTg5Njc5NjE5NTQ3NzUiLCJhdWQiOlsiYm9va21hcmsiLCJodHRwczovL3JheWFuLWRldi51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA0NzczNDIzLCJleHAiOjE2MDQ4NTk4MjMsImF6cCI6Ikp3aGJrVDJMQ3M2NmwzbDNZaDhROFBKNEhGdjd4bmhiIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpjYXRlZ29yaWVzIiwicG9zdDpib29rbWFya3MiXX0.xKD7XRzr01rpGh3aFKKEmd7Zhruhw45ba0QyVc3KI4NftyNm3YrhIpfQNMLy0wPPyzS--wlz4f-8MjB8oH_KNVebDELP6PkNupbnUiL989IJ2s1qh29CJcRlojalVfL7AKpekivZI7L0bXYQhbVko_MqmtxD8I7TJ9ZUKE_ALWWZxOyz0mvFrCHg1Gej0Xp3Gi3YtcJl57drMHWkSZtyRtYoQoRJFUN013zkxfRQmxYmgsSCos5qjl_MtaH2eJ4o9kFoulOMBGMlAM1faKNIfG6AOsduzNwFV9fi7pXYiysLCVpIVRKXuj-nowfRSoEKmMpNBw3dVCSvXRdrCKoUiw'


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

        #! Increment bookmark_id before execution
        bookmark_id = 5

        self.headers.update({'Authorization': 'Bearer ' + str(admin_token)})

        res = self.client().patch(
            '/bookmarks/' + str(bookmark_id), json=self.new_bookmark, headers=self.headers)
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

        #! Increment bookmark_id before execution
        bookmark_id = 9

        self.headers.update({'Authorization': 'Bearer ' + str(user_token)})

        res = self.client().delete('/bookmarks/' + str(bookmark_id), headers=self.headers)
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
