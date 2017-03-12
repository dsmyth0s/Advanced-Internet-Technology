from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	__tablename__= 'restaurant'
	id = Column(Integer, primary_key = True)
	restaurant_name = Column(String)
	restaurant_address = Column(String)
	restaurant_image = Column(String)
	venue_id = Column(String)
	restaurant_mealType = Column(String)
	restaurant_location = Column(String)

	#Add a property decorator to serialize information from this database
	@property
	def serialize(self):
		return {
			'restaurant_name': self.restaurant_name,
			'restaurant_address': self.restaurant_address,
			'restaurant_image' : self.restaurant_image,
			'id' : self.id,
			'venue_id' : self.venue_id,
			'restaurant_mealType': self.restaurant_mealType,
			'restaurant_location': self.restaurant_location
		}

#Creates a local sqlite db file in folder
engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)