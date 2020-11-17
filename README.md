# URL Bookmark
[![made-with-python](https://img.shields.io/badge/Backend-Python-1F425F.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-Green.svg)](https://opensource.org/licenses/MIT)

A RESTful API that provides Bookmarked URLs to visit later.

The backend code follows [PEP-8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

### Getting Started
- Base URL: `https://url-bookmark.herokuapp.com/`

- Authentication: `https://bit.ly/2Ipsvrl`

It's recommended to run the project inside a virtual environment. To do this, run the following:

```
virtualenv venv (For first time only)
source venv/bin/activate
```

From the `/backend` folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application, run the following commands inside the `/backend` folder:

```
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```
For `Windows` system, replace `export` command with `set` (e.g. `set FLASK_APP=api.py`)

**Frontend** (Not Applicable currently)

If applicable; inside the `/frontend` folder, run the following commands to start the client:

```
npm install // Only once to install dependencies
npm start
```

By default, the frontend will run on `localhost:3000`.

**Tests**

To run tests, go back to the `project` folder and run the following commands:

```
dropdb bookmark_test
createdb bookmark_test
python unit_tests.py
```

Omit the `dropdb` command for the first time running the tests.

### Roles and Permissions
The current permissions are: `get:categories`, `post:bookmarks`, `patch:bookmarks`, and `delete:bookmarks`.
The current roles for this web app are `user` and `admin` in the following arrangement:
- `user` role has the following permissions: `get:categories` and `post:bookmarks`.
- `admin` role has *all* the permissions listed above.

### Error Handling
Errors are returned as JSON obejcts in the following format:

```json
{
  "error": 404, 
  "message": "not found",
  "success": false
}
```

The Error types the API returns when requests fail are:
| HTTP Status Code | Response |
| ----------- | ----------- |
| 400 | Bad Request |
| 401 | Auth Error |
| 403 | Unauthorized |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 422 | Unprocessable Entity |

### Endpoints
**GET /bookmarks**

Returns a list of bookmarked URLs. Results are paginated in groups of 5. Include a query argument to choose page number (e.g. `?page=1`).

* Sample Request:

```
curl -X GET https://url-bookmark.herokuapp.com/bookmarks
```

* Sample Response:

```json
{
    "bookmarks": [
        {
            "id": 1,
            "title": "Personal Site",
            "url": "https://rayan.dev"
        },
        {
            "id": 2,
            "title": "Saudi Network Information Center",
            "url": "https://nic.sa"
        },
        {
            "id": 3,
            "title": "Work Site",
            "url": "https://citc.gov.sa"
        },
        {
            "id": 4,
            "title": "GitHub Account",
            "url": "https://github.com/RayanAlkhelaiwi"
        },
        {
            "id": 5,
            "title": "Twitter",
            "url": "https://twitter.com"
        }
    ],
    "success": true
}
```

**GET /categories**

Returns a list of categories of the bookmarks and their importance. Results are paginated in groups of 5. Include a query argument to choose page number (e.g. `?page=1`).

* Sample Request:

```
curl -X GET https://url-bookmark.herokuapp.com/categories
```

* Sample Response:

```json
{
    "categories": [
        {
            "id": 1,
            "important": false,
            "type": "Personal"
        },
        {
            "id": 2,
            "important": true,
            "type": "Work"
        }
    ],
    "success": true
}
```

**POST /bookmarks**

Creates a new URL bookmark by submitting the information for a title and its URL. It returns the submitted information, success value and the stored bookmarks.

* Sample Request:

```
curl -X POST -H "Content-Type: application/json" -d '{"title":"Personal Site", "url":"https://rayan.dev"}' https://url-bookmark.herokuapp.com/bookmarks
```

* Sample Response:

```json
{
    "bookmarks": [
        {
            "id": 1,
            "title": "Saudi Network Information Center",
            "url": "https://nic.sa"
        },
        {
            "id": 2,
            "title": "Work",
            "url": "https://citc.gov.sa"
        },
        {
            "id": 3,
            "title": "GitHub Account",
            "url": "https://github.com/RayanAlkhelaiwi"
        },
        {
            "id": 4,
            "title": "Twitter",
            "url": "https://twitter.com"
        },
        {
            "id": 5,
            "title": "Personal Site",
            "url": "https://rayan.dev"
        }
    ],
    "created": {
        "id": 5,
        "title": "Personal Site",
        "url": "https://rayan.dev"
    },
    "success": true
}
```

**PATCH /bookmarks/{bookmark_id}**

Updates the bookmark info using the bookmark's ID. Returns the ID of the deleted bookmark and the success value.

* Sample Request:

```
curl -X PATCH -H "Content-Type: application/json" -d '{"title":"Personal Site", "url":"https://rayan.dev"}' https://url-bookmark.herokuapp.com/bookmarks/5
```

* Sample Response:

```json
{
    "bookmark": {
        "id": 5,
        "title": "Personal Site",
        "url": "https://rayan.dev"
    },
  "success": true
}
```

**DELETE /bookmarks/{bookmark_id}**

Deletes the bookmark with the given ID. Returns the ID of the deleted bookmark and the success value.

* Sample Request:

```
curl -X DELETE https://url-bookmark.herokuapp.com/bookmarks/4
```

* Sample Response:

```json
{
  "deleted": 4,
  "success": true
}
```
