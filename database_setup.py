import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Users(Base):
    __tablename__ = 'users'
   
    id = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    keyword = Column(String(250), nullable=False)
    carrito_total = Column(Integer, nullable=True)

    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'id'         : self.id,
       }
 
class Products(Base):
    __tablename__ = 'products'


    name =Column(String(80), nullable = False)
    id = Column(String(250), primary_key = True)
    description = Column(String(250))
    price = Column(Integer)
    size = Column(String(250))
    brand = Column(String(250))
    color = Column(String(250))

    #We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'size'         : self.size,
           'brand'         : self.brand,
           'color'         : self.color,
       }


class ShoppingCart(Base):
    __tablename__ = 'Shopping_Cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    total = Column(Integer)
    user_id = Column(String(250), ForeignKey('users.id'))
    user = relationship(Users)

class tokenBlackList(Base):
    __tablename__ = 'tokenBlackList'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(250), nullable=False)
    


 

engine = create_engine('sqlite:///demostore_flask.db?check_same_thread=False')
 

Base.metadata.create_all(engine)