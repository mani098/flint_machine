from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from flint_engine import db


class LoginModel(db.Model):

	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String(50))  # username
	password = Column(String(64))  # hashed with md5

	def __repr__(self):
		return '<User %r>' % (self.username)

	def save(self):
		db.session.add(self)


class MyOrderModel(db.Model):

	__tablename__ = "myorders"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), index=True)
	users = relationship("LoginModel")
	order = Column(String(500))

	def __repr__(self):
		return '<User %r>' % (self.userid)

	def save(self):
		db.session.add(self)


class FoodItems(db.Model):

	__tablename__ = "food_items"

	id = Column(Integer, primary_key=True)
	food_name = Column(String(50))

	def __repr__(self):
		return "<Food %r" % (self.food_name)

	def save(self):
		db.session.add(self)


class FoodIngredients(db.Model):

	__tablename__ = "food_ingredients"

	id = Column(Integer, primary_key=True)

	food_id = Column(Integer, ForeignKey("food_items.id"), index=True)
	food_items = relationship("FoodItems")
	ingredient_type = Column(String(35))
	ingredient_value = Column(String(40))
	price = Column(Float)
	subcategory = Column(Boolean, default=False)  # does sub category exists
	input_type = Column(String(5)) 				 # radio or check
	parent_id = Column(Integer, default=0)  # id of same table

	def __repr__(self):
		return "<Food %r" % (self.ingredient_type)

	def save(self):
		db.session.add(self)


def commit():
	db.session.commit()
