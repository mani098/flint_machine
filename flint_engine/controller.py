import json
import hashlib
from flask import session
from models import FoodItems, FoodIngredients, LoginModel, MyOrderModel, commit
from flint_engine.__init__ import db


def login(username, password):
	"""logins the user if already exists or creates new row in users table for the new user"""

	password_hash = hashlib.md5(password)
	password = password_hash.hexdigest()
	try:
			user = db.session.query(LoginModel).filter(LoginModel.username == username).first()
			if user.username == username and user.password == password:
				return "success"
			elif user.username == username and user.password != password:
				return "Password is wrong"
	except:
		user = LoginModel()
		user.username = username
		user.password = password
		user.save()
		commit()
		return "success"


def cache_orders(form_data):
	session_name = str(form_data.get("item_name")) + "_order"
	order_price = str(form_data.get("item_name")) + "_price"
	if not session.has_key(session_name):
		orders = {}
		for data in form_data:
			if data != "item_name":
				if data.endswith("_check"):
					orders[data[:-6]] = form_data.getlist(data)
				else:
					orders[data] = form_data.get(data)
		session[session_name] = json.dumps(orders)
		session[order_price] = form_data.get("sub_total")


def save_orders():
	username = session.get("username")
	user_id = db.session.query(LoginModel.id).filter(LoginModel.username == username).first()[0]
	new_order = MyOrderModel()
	saved_orders = []

	for item in session:
		if item.endswith("_order"):
			placed_items = json.dumps({item[:-6]: session.get(item)})
			new_order.user_id = user_id
			new_order.order = placed_items
			new_order.save()
			saved_orders.append(item)
	commit()

	return saved_orders


def get_orders():
	username = session.get("username")
	user_id = db.session.query(LoginModel.id).filter(LoginModel.username == username).first()[0]
	orders_data = []
	orders = db.session.query(MyOrderModel.order).filter(MyOrderModel.user_id == user_id).all()
	for order in orders:
		orders_data.append(json.loads(order.order))
	return orders_data


def get_food_items():
	records = db.session.query(FoodItems).all()
	food_items = [(record.food_name).replace("_", " ") for record in records]
	return food_items


def get_food_data(food_item):
	ingredients = []

	food = db.session.query(FoodItems).filter(FoodItems.food_name == food_item).scalar()
	ingredient_types = db.session.query(FoodIngredients.ingredient_type, FoodIngredients.subcategory).filter(FoodIngredients.food_id == food.id).distinct()
	for ingredient in ingredient_types:
		datas = db.session.query(FoodIngredients.ingredient_value, FoodIngredients.input_type, FoodIngredients.subcategory, FoodIngredients.id, FoodIngredients.price)\
				.filter(FoodIngredients.ingredient_type == ingredient[0], FoodIngredients.food_id == food.id).distinct()
		sub_ingredients = []
		for data in datas:
			if int(data[2]) == 1:
				sub_datas = db.session.query(FoodIngredients.ingredient_type, FoodIngredients.ingredient_value, FoodIngredients.input_type, FoodIngredients.price).\
				filter(FoodIngredients.parent_id == data[3]).all()
				sub_ingredients.append(dict(main_ingredients=data, sub_ingredients=sub_datas))
			else:
				sub_ingredients.append(data)
		tmp_data = dict(ingredient=ingredient, ingredient_value=sub_ingredients)
		ingredients.append(tmp_data)
	return ingredients


def price_data():

	with open("./flint_engine/price.json", "r") as price:
		prices = json.loads(price.read())
		return prices


def update_price():
	prices = price_data()
	if prices["flag"] == 1:
		records = db.session.query(FoodItems).all()
		for record in records:
			ingredients = db.session.query(FoodIngredients.ingredient_type, FoodIngredients.ingredient_value, FoodIngredients.subcategory)\
							.filter(FoodIngredients.food_id == record.id).all()
			# for ingredient in ingredients:
			# 	for p_data in prices[record.food_name]["ingredients"]:
			# 		if p_data == ingredient[1] and ingredient[2] == False:
			pass
