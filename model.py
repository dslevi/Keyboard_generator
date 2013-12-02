import config
import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Table

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
    right_hand = Column(Boolean, default=True)
    occupation = Column(String(64), nullable=False)
    age = Column(Integer, nullable=True)
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
    input1 = Column(Text, nullable=False)
    input2 = Column(Text, nullable=False)
    mistakes = Column(Text, nullable=False)
    wpm = Column(Text, nullable=False)
    accuracy = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    kd_id = Column(Integer, ForeignKey("keyboards.id"))

    kb = relationship("Keyboard")
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
    rating = Column(Integer, nullable=True, default=0)
    keys = relationship("Key", uselist=True)
    tests = relationship("TestAnalytic", uselist=True)
    analytics = relationship("Analytics", uselist=True)

    user = relationship("User")

class Key(Base):
    __tablename__="keys"
    id = Column(Integer, primary_key=True)
    location = Column(Text, nullable=False)
    values = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    kb_id = Column(Integer, ForeignKey("keyboards.id"))

    keyboard = relationship("Keyboard")

class Text(Base):
    __tablename__="text"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    title = Column(Text, nullable=False)

class TestAnalytic(Base):
    __tablename__="testAnalytics"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    wpm = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    keyboard_id = Column(Integer, ForeignKey("keyboards.id"))

    keyboard = relationship("Keyboard")

#Database creation methods

def create_tables():
    Base.metadata.create_all(engine)
    u = User(name="Guest", email="test@test.com", occupation="programmer")
    u.set_password("guest")
    session.add(u)
    d = User(name="Danielle", email="d@hba.com", occupation="Programmer")
    d.set_password("python")
    session.add(d)
    a = Analytics(input1="input1", input2="input2", user_id=u.id, mistakes="mistakes", wpm="wpm", accuracy="accuracy")
    u.analytics.append(a)
    session.commit()

def create_QWERTY():
    locations = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'B01', 'B02', 'B03', 
                'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 
                'C09', 'C10', 'C11', 'C12', 'C13', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11','E04']

    codes = [192, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 189, 187, 8,
            9, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 219, 221, 220,
            65, 83, 68, 70, 71, 72, 74, 75, 76, 186, 222, 13,
            90, 88, 67, 86, 66, 78, 77, 190, 188, 190, 32]

    values = ['` ~', '1 !', '2 @', '3 #', '4 $', '5 %', '6 ^', '7 &', '8 *', '9 (', '0 )', '- _', '= +', 'DELETE DELETE',
            'TAB TAB', 'q Q', 'w W', 'e E', 'r R', 't T', 'y Y', 'u U', 'i I', 'o O', 'p P', '[ {', '] }', '\\ |',
            'a A', 's S', 'd D', 'f F', 'g G', 'h H', 'j J', 'k K', 'l L', '; :', '\' "', 'ENTER ENTER', 'z Z', 'x X', 'c C', 'v V', 'b B', 'n N', 'm M', ', <', '. >', '/ ?','SPACE SPACE']

    k = Keyboard(name="QWERTY", user_id=0)
    session.add(k)
    for i in range(len(locations)):
        key = Key(kb_id=k.id)
        key.location = locations[i]
        key.values = values[i]
        key.code = codes[i]
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

def create_texts(filename):
    count = 0
    f = open(filename)
    for line in f:
        tokens = line.strip().split("|")
        t = Text(content=tokens[0], title=tokens[1], author=tokens[2])
        session.add(t)
        count += 1
    session.commit()
    print "Prompts: ", count



if __name__ == "__main__":
    create_tables()
    create_QWERTY()
    create_prompts("prompts.txt")
    create_texts("textsamples.txt")