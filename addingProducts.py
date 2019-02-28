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


#----------Store items----------------

# Polo_Shirt

storeProduct1 = Products(name="IZOD Polo Shirt", id = "IZD_PS", description = "IZOD polo type shirt", 
                     price = 25, size = "M", brand = "IZOD", color = "Navy" )

session.add(storeProduct1)
session.commit()

storeProduct2 = Products(name="Nautica Polo Shirt", id = "NTA_PS", description = "Nautica polo type shirt", 
                     price = 30, size = "L", brand = "Nautica", color = "White" )

session.add(storeProduct2)
session.commit()

storeProduct3 = Products(name="Levis 505 Jeans", id = "LVS_BJ", description = "Levis 505 jeans", 
                     price = 40, size = "32x32", brand = "Levis", color = "Midnight Blue" )

session.add(storeProduct3)
session.commit()

storeProduct4 = Products(name="Polo Shirt2", id = "GAP_LJ", description = "GAP loose type jeans", 
                     price = 35, size = "32x30", brand = "GAP", color = "Washed Blue" )

session.add(storeProduct4)
session.commit()






