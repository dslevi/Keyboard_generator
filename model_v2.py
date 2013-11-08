# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship, backref

# ENGINE = create_engine("sqlite:///keyboard.db", echo= False)
# session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

# Base = declarative_base()
# Base.query = session.query_property()

class Key_value(object):
    def __init__(self, key_id, code, key_value, key_location):
        #primary key
        self.id = key_id
        self.code = code
        self.key_value = key_value
        #belongs to key_location object, one-to-one
        self.key_location = key_location

class Key_location(object):
    def __init__(self, loc_id, location, value, keyboard):
        #primary key
        self.id = loc_id
        #physical location of key on keyboard, regardless of input value
        self.id = location
        #key_value object, one-to-one
        self.value = value
        #belongs to keyboard object
        self.keyboard = keyboard

class Keyboard(object):
    def __init__(self, board_id, user_id, keys):
        #primary key
        self.id = board_id
        self.user = user_id
        #array of key_location objects
        self.keys = keys

class User(object):
    def __init__(self, user_id, username, password, email, bigrams, key_weights, key_times, preferences):
        self.id = user_id
        self.username = username
        self.password = password
        self.email = email
        #user can have many keyboards, one-to-many relationship
        #data about user that is used to generate keyboards
        #array of bigrams
        self.bigrams = bigrams
        self.key_weights = key_weights
        self.key_times = key_times
        self.preferences = preferences

class Keypress(object):
#     __tablename__="keypresses"
    def __init__(self, press_id, key_value, timestamp, bigram):
        self.id = press_id
        self.key_value = key_value
        self.timestamp = timestamp
        self.bigram = bigram
