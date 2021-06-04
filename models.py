from peewee import *
from flask_login import UserMixin
import os
from playhouse.db_url import connect

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///insight.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()
    follow_list=CharField(null=True, default={})
    
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    print("Connected to the DB and created unique tables")
    
    DATABASE.close()