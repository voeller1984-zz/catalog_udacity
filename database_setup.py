import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250))
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'name'      : self.name,
            'email'     : self.email, 
            'picture'   : self.picture, 
            'id'        : self.id,
        }


class Category(Base):
    __tablename__ = 'category'
    
    name = Column(String(80), primary_key=True)


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), primary_key=True)
    itemCategory = Column(String(80), ForeignKey('category.name'))
    description = Column(String(2000))
    time = Column(DateTime, server_default=func.now())
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    user = relationship(User)
    

# serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'category': self.itemCategory,
        }

engine = create_engine('postgresql://catalog:serginho@localhost/catalog')


Base.metadata.create_all(engine)
