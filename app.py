import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, Bookmark, Category
from auth import AuthError, requires_auths

items_per_page = 5
def pagination(request, selection):
    '''
        To specify the number of items of both bookmarks and categories to display per page
    '''
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * items_per_page
    end = start + items_per_page

    items = [item.format() for item in selection]
    current_items = items[start:end]

    return current_items

app = Flask(__name__)
setup_db(app)
CORS(app)

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
#     return response

# Endpoints

@app.route('/')
def index():
    '''
        GET /
            Primary endpoint for index page
    '''
    return get_bookmarks()


@app.route('/bookmarks')
# @requires_auth('get:bookmarks')
def get_bookmarks():
    '''
        GET /bookmarks
            Endpoint to fetch available bookmarks
    '''
    bookmarks = [bookmark for bookmark in Bookmark.query.all()]
    paginated_bookmarks = pagination(request, bookmarks)

    if len(paginated_bookmarks) == 0:
        return not_found(404)

    return jsonify({
        'success': True,
        'bookmarks': paginated_bookmarks
    })


@app.route('/categories')
@requires_auth('get:categories')
def get_categories(jwt):
    '''
        GET /categories
            Private endpoint to list the categories of the bookmarks and their importance
            With 'get:categories' permission
    '''
    categories = [category for category in Category.query.all()]
    paginated_categories = pagination(request, categories)

    if len(paginated_categories) == 0:
        return not_found(404)

    return jsonify({
        'success': True,
        'categories': paginated_categories
    })


@app.route('/bookmarks', methods=['POST'])
@requires_auth('post:bookmarks')
def create_bookmark(jwt):
    '''
        POST /bookmarks
            Private endpoint to submit a url as a bookmark
            With 'post:bookmarks' permission
    '''
    body = request.get_json()

    new_title = body.get('title', None)
    new_url = body.get('url', None)

    try:
        bookmark = Bookmark(title=new_title, url=new_url)
        bookmark.insert()

        bookmarks = [bookmark.format() for bookmark in Bookmark.query.all()]

        return jsonify({
            'success': True,
            'created': bookmark.format(),
            'bookmarks': bookmarks
        })
    except:
        return unprocessable(422)


@app.route('/bookmarks/<int:id>', methods=['PATCH'])
@requires_auth('patch:bookmarks')
def update_bookmark(jwt, id):
    '''
        PATCH /bookmarks
            Private endpoint to update a bookmark
            With 'patch:bookmarks' permission
    '''
    try:
        bookmark = Bookmark.query.filter(Bookmark.id == id).one_or_none()

        if bookmark is None:
            return not_found(404)
        body = request.get_json()

        title = body.get('title')
        url = body.get('url')

        bookmark.title = title
        bookmark.url = url

        bookmark.update()

        return jsonify({
            'success': True,
            'bookmark': bookmark.format()
        })

    except:
        return unprocessable(422)


@app.route('/bookmarks/<int:id>', methods=['DELETE'])
@requires_auth('delete:bookmarks')
def delete_bookmark(jwt, id):
    '''
        DELETE /bookmarks
            Private endpoint to delete a bookmark
            With 'delete:bookmarks' permission
    '''
    try:
        bookmark = Bookmark.query.filter(Bookmark.id == id).one_or_none()

        if bookmark is None:
            return not_found(404)

        bookmark.delete()

        return jsonify({
            'success': True,
            'deleted': id
        })

    except:
        return unprocessable(422)


# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    '''
        Error handler for unprocessable entity, 422
    '''
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(405)
def not_found(error):
    '''
        Error handler for method not allowed, 405
    '''
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(404)
def not_found(error):
    '''
        Error handler for not found entity, 404
    '''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(auth_error):
    '''
        Error handler for AuthError entity, 401
    '''
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error
    }), 401

