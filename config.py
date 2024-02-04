# config.py

import os

class Config(object):
    SECRET_KEY =  'secret-key' 
    SQLALCHEMY_DATABASE_URI =  'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
