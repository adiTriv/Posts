import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# for mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# config code - sets up all the dependencies for our ORM
Base = declarative_base()
# Base is our base class that has all the features of SQLAlchamy

# class code - representation of tables in the form of objects
# inherited from Base so that sqlalchamy can know these are special class representing our tables
class Users(Base):
    # contains all the code for tables and also for mapper

    # table code
    __tablename__ = 'users'

    # mapper code - creates attrs that are used to create columns in our tables 
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, primary_key=True)
    about = Column(String(250))

    @property
    def serialize(self):
        # return serialized json data
        return {
            'name': self.name,
            'about': self.about,
            'user_id': self.user_id,
        }




class Posts(Base):
    __tablename__ = 'posts'

    head = Column(String(100), nullable=False)
    post = Column(String(500), nullable=False)
    author = Column(String(80), nullable=False)
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    # relationship
    sp_users = relationship(Users)

    @property
    def serialize(self):
        # return serialized json data
        return {
            'head': self.head,
            'post': self.post,
            'author': self.author,
            'post_id': self.post_id,
            'user_id': self.user_id,
        }
     


engine = create_engine('sqlite:///postApp.db')
# makes a database file or communicate to one. 

Base.metadata.create_all(engine)
# accepts a database and creates the tables specified in above classes
# and adds them to the database just created 
