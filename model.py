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

def create_tables():
    Base.metadata.create_all(engine)
    u = User(name="Tester", email="test@test.com", occupation="programmer", age=23, right_hand="true")
    u.set_password("unicorn")
    session.add(u)
    a = Analytics(text="This is a test post", raw_text="This is the raw_text of a test post.", 
        strokes="test", user_id=u.id)
    u.analytics.append(a)
    session.commit()

def create_prompts(filename):
    f = open(filename)
    for line in f:
        p = Prompts(text=unicode(line))
        session.add(p)
    session.commit()

# if __name__ == "__main__":
#     create_tables()
#     create_prompts("prompts.txt")
