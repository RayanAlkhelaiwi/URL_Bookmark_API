import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import setup_db, Bookmark, Category
from .auth.auth import AuthError, requires_auth

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
    bookmarks = [bookmark.format() for bookmark in Bookmark.query.all()]

    if len(bookmarks) == 0:
        return not_found(404)

    return jsonify({
        'success': True,
        'bookmarks': bookmarks
    })


@app.route('/categories')
@requires_auth('get:categories')
def get_categories(jwt):
    '''
        GET /categories
            Private endpoint to list the categories of the bookmarks and their importance
            With 'get:categories' permission
    '''
    categories = [category.format() for category in Category.query.all()]

    if len(categories) == 0:
        return not_found(404)

    return jsonify({
        'success': True,
        'categories': categories
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
            'created': bookmark,
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
            'bookmark': bookmark
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
