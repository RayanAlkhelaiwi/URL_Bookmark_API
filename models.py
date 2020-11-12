import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "bookmark"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
        Binds a flask application with SQLAlchemy
    '''

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    db.create_all()


# Database Models

class Bookmark(db.Model):
    '''
        Table to bookmark URLs
    '''
    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    # category_id = Column(Integer, ForeignKey('Category.id'))
    # category = relationship('category', foreign_keys=category_id)

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url
        }


class Category(db.Model):
    '''
        Table to categorise bookmarked and determine its importance to read
    '''
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category_type = Column(String)
    is_important = Column(Boolean)

    def __init__(self, category_type, is_important):
        self.category_type = category_type
        self.is_important = is_important

    def format(self):
        return {
            'id': self.id,
            'type': self.category_type,
            'important': self.is_important
        }
