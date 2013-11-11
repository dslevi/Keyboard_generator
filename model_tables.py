import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin


engine = create_engine(config.DB_URI, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class User(Base, UserMixin):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)
    analytics = relationship("Analytics", uselist=True)
    right_hand = Column(String(10), nullable=False)
    occupation = Column(String(64), nullable=False)
    age = Column(Integer)
    keyboard = relationship("Keyboard", uselist=True)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    raw_text = Column(Text, nullable=False)
    strokes = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

class Prompts(Base):
    __tablename__="prompts"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

class Keyboard(Base):
    __tablename__="keyboards"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    keys = relationship("Key", uselist=True)

    user = relationship("User")

class Key(Base):
    __tablename__="keys"
    id = Column(Integer, primary_key=True)
    div = relationship("Key_Div", uselist=False)
    location = relationship("Key_Location", uselist=False)
    values = relationship("Key_Value", uselist=True)
    codes = relationship("Key_Code", uselist=True)
    kb_id = Column(Integer, ForeignKey("keyboards.id"))

    keyboard = relationship("Keyboard")

class Key_Location(Base):
    __tablename__="key_location"
    id = Column(Integer, primary_key=True)
    #should have a many to many relationship?
    key_id = Column(Integer, ForeignKey("keys.id"))
    location = Column(Text, nullable=False)

    key = relationship("Key")

class Key_Value(Base):
    __tablename__="key_values"
    id = Column(Integer, primary_key=True)
    #should have a many to many relationship?
    key_id = Column(Integer, ForeignKey("keys.id"))
    value = Column(Text, nullable=False)

    key = relationship("Key")

class Key_Code(Base):
    __tablename__="key_codes"
    id = Column(Integer, primary_key=True)
    #should have a many to many relationship?
    key_id = Column(Integer, ForeignKey("keys.id"))
    code = Column(Text, nullable=False)

    key = relationship("Key")

class Key_Div(Base):
    __tablename__="divs"
    id = Column(Integer, primary_key=True)
    #should have a many to many relationship?
    key_id = Column(Integer, ForeignKey("keys.id"))
    name = Column(Text, nullable=False)

    key = relationship("Key")





#Database creation methods

def create_tables():
    Base.metadata.create_all(engine)
    u = User(name="Guest", email="test@test.com", occupation="programmer", age=23, right_hand="true")
    u.set_password("guest")
    session.add(u)
    a = Analytics(text="This is a test post", raw_text="This is the raw_text of a test post.", 
        strokes="test", user_id=u.id)
    u.analytics.append(a)
    session.commit()

def create_QWERTY():
    #should these have separate joined tables or should they be represented as strings and then parsed into lists
    locations = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'B01', 'B02', 'B03', 
                'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 
                'C09', 'C10', 'C11', 'C12', 'C13', 'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'E01', 'E03', 'E04']

    divs = ["tilde", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero", "dash", "plus", "delete",
            "tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "brace_open", "brace_close", "pipe",
            "caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", "colon", "quote", "enter",
            "shift", "Z", "X", "C", "V", "B", "N", "M", "comma", "period", "question",
            "control", "alt", "space"]

    codes = [[126, 96], [33, 49], [64, 50], [35, 51], [36, 52], [37, 53], [94, 54], [38, 55], [42, 56], [40, 57], [41, 48], [95, 45], [43, 61], [8],
            [9], [81, 113], [87, 119], [69, 101], [82, 114], [84, 116], [89, 121], [85, 117], [73, 105], [79, 111], [80, 112], [123, 91], [125, 93], [124, 92],
            [20], [65, 97], [83, 115], [68, 100], [70, 102], [71, 103], [72, 104], [74, 106], [75, 107], [76, 108], [58, 59],  [34, 39], [13],
            [16], [90, 122], [88, 120], [67, 99], [86, 118], [66, 98], [78, 110], [77, 109], [60, 44], [62, 46], [63, 47],
            [17], [18], [32]]

    values = [['`', '~'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'], ['5', '%'], ['6','^'], ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['-', '_'], ['=', '+'], ['delete'],
            ['tab'], ['q', 'Q'], ['w', 'W'], ['e', 'E'], ['r', 'R'], ['t', 'T'], ['y', 'Y'], ['u', 'U'], ['i', 'I'], ['o', 'O'], ['p', 'P'], ['[', '{'], [']', '}'], ['\\', '|'],
            ['caps'], ['a', 'A'], ['s', 'S'], ['d', 'D'], ['f', 'F'], ['g', 'G'], ['h', 'H'], ['j', 'J'], ['k', 'K'], ['l', 'L'], [';', ':'], ['\'', '"'], ['enter'],
            ['shift'], ['z', 'Z'], ['x', 'X'], ['c', 'C'], ['v', 'V'], ['b', 'B'], ['n', 'N'], ['m', 'M'], [',', '<'], ['.', '>'], ['/', '?'],
            ['control'], ['alt'], ['space']]

    k = Keyboard(name="QWERTY", user_id=0)
    session.add(k)
    for i in range(len(locations)):
        key = Key(kb_id=k.id)
        l = Key_Location(location=locations[i], key_id=key.id)
        key.location = l
        d = Key_Div(name=divs[i], key_id=key.id)
        key.div = d
        for value in values[i]:
            v = Key_Value(value=value, key_id=key.id)
            key.values.append(v)
        for code in codes[i]:
            c = Key_Code(code=code, key_id=key.id)
            key.codes.append(c)
        k.keys.append(key)
    session.commit()
    print "QWERTY board created"

def create_prompts(filename):
    count = 0
    f = open(filename)
    for line in f:
        if len(line) <= 95:
            p = Prompts(text=unicode(line))
            session.add(p)
            count += 1
    session.commit()
    print "Prompts: ", count

# if __name__ == "__main__":
    # create_tables()
    # create_QWERTY()
    # create_prompts("prompts.txt")
    