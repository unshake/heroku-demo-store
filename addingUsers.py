from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Users, Products, ShoppingCart, Base

engine = create_engine('sqlite:///demostore_flask.db?check_same_thread=False')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()








#-------------------Users Registration--------------------------
user1 = Users(name="Edgar Martinez", id = "monolet@hotmail.com", password = "*Monolet", keyword = 'mi_palabra', carrito_total = 0)

session.add(user1)
session.commit()

user2 = Users(name="Rene Mejia", id="monolet@gmail.com", password="*Monolet", keyword = 'mi_palabra', carrito_total=0)
session.add(user2)
session.commit()

user3 = Users(name="John Cuevas", id = "john@cuevas.com", password = "*Cuevitas", keyword = 'deer', carrito_total = 0)

session.add(user3)
session.commit()

user4 = Users(name="Peluso Perro", id="peluso@perro.com", password="*Pelusos", keyword = 'canino', carrito_total=0)
session.add(user4)
session.commit()

