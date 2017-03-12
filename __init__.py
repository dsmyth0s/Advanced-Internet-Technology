from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/app/v1/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
	if request.method == 'GET':
		# RETURN ALL RESTAURANTS IN DATABASE
		restaurants = session.query(Restaurant).all()
		return jsonify(restaurants = [i.serialize for i in restaurants])

	elif request.method == 'POST':
		# MAKE A NEW RESTAURANT AND STORE IT IN DATABASE
		location = request.json['location']
		mealType = request.json['mealType']    
		restaurant_info = findARestaurant(mealType, location)
		r_message = {"message":"No Restaurants Found"}
		# Condition for taking the dictionary stored in the array and populating the fields in DB
		if restaurant_info[0] != r_message:
			for r in range(len(restaurant_info)):
				rest_data = restaurant_info[r]
				restaurant = Restaurant(**restaurant_info[r])
				session.add(restaurant)
				session.commit() 
			return jsonify(restaurant = restaurant_info)
		else:
			# Store parameters as a proper noun
			meal = mealType.capitalize()
			loc = location.capitalize()
			# Return error messages
			return jsonify({"Error":"No Restaurants Found for %s in %s" % (meal, loc)})


    
@app.route('/app/v1/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	restaurant = session.query(Restaurant).filter_by(id = id).one()
	if request.method == 'GET':
		#RETURN A SPECIFIC RESTAURANT
		return jsonify(restaurant = restaurant.serialize)
	elif request.method == 'PUT':
		#UPDATE A SPECIFIC RESTAURANT
		address = request.args.get('address')
		image = request.args.get('image')
		name = request.args.get('name')
		if address:
			restaurant.restaurant_address = address
		if image:
			restaurant.restaurant_image = image
		if name:
			restaurant.restaurant_name = name
		session.commit()
		return jsonify(restaurant = restaurant.serialize)
	elif request.method == 'DELETE':
		#DELETE A SPECFIC RESTAURANT
		session.delete(restaurant)
		session.commit()
		return "Restaurant Deleted"


@app.route('/app/v1/location/<string:location>', methods = ['GET', 'DELETE'])
def location_handler(location):
	restaurant = session.query(Restaurant).filter_by(restaurant_location = location).all()
	if request.method == 'GET':
		#RETURN A LIST OF RESTAURANTS BY LOCATION
		return jsonify(restaurant = restaurant.serialize)
	elif request.method == 'DELETE':
		#DELETE RESTAURANT BY LOCATION
		session.delete(restaurant)
		session.commit()
		return "Restaurant(s) Deleted"

@app.route('/app/v1/meal/<string:meal>', methods = ['GET', 'DELETE'])
def meal_handler(meal):
	restaurant = session.query(Restaurant).filter_by(restaurant_mealType = location).all()
	if request.method == 'GET':
		#RETURN A LIST OF RESTAURANTS
		return jsonify(restaurant = restaurant.serialize)
	elif request.method == 'DELETE':
		#DELETE RESTAURANT BY LOCATION BY LOCATION
		session.delete(restaurant)
		session.commit()
		return "Restaurant(s) Deleted"

    

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)