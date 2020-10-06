import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "url_shortener"
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


class long_url(db.Model):
    '''
        Long/Original URL to be shorten
    '''
    __tablename__ = 'long_url'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    short_url_id = Column(Integer, ForeignKey('short_url.id'))
    short_url = relationship('short_url', foreign_keys=short_url_id)

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url

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
            'url': self.url,
            'short_url': self.short_url
        }


class short_url(db.Model):
    '''
        Shorten URL of the long/original URL (To be directed tos)
    '''
    __tablename__ = 'short_url'

    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __init__(self, url):
        self.url = url

    def format(self):
        return {
            'id': self.id,
            'short_url': self.url
        }
