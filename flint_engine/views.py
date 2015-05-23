import json
from flask.ext.classy import FlaskView, route
from flask import render_template, url_for, jsonify, session, redirect, request


class DashboardView(FlaskView):

	@route("/")
	def home_view(self):
		import controller
		food_items = controller.get_food_items()
		return render_template("home.html", food_menu=food_items)

	@route("/item/<string:page_alias>")
	def food_items_view(self, page_alias):
		import controller
		food_items = controller.get_food_items()
		food_name = page_alias.replace("_", " ")
		if food_name in food_items:
			ingredients = controller.get_food_data(page_alias)
			data = dict(food_name=food_name, ingredients=ingredients)
			return render_template("item.html", data=data)

	@route("/login", methods=["POST", "GET"])
	def login_view(self):
		import controller
		message = ""
		if session.get("username"):
			if int(session.get("n_orders")) > 1:
				return redirect(url_for('DashboardView:checkout_view'))
			else:
				return redirect(url_for('DashboardView:home_view'))
		else:
			if request.method == 'POST':
				username = request.form.get("username")
				password = request.form.get("password")
				login_status = controller.login(username, password)
				if login_status == "success":
					session["username"] = username
					if session.get("n_orders"):
						return redirect(url_for('DashboardView:checkout_view'))
					else:
						return redirect(url_for('DashboardView:home_view'))
				else:
					message = login_status
					return render_template('login.html', message=message)

		return render_template("login.html", message=message)

	@route("/placeorder", methods=["POST", "GET"])
	def place_order_view(self):
		import controller
		if request.form:
			controller.cache_orders(request.form)
		# session_name = str(request.form.get("item_name")) + "_order"
		# return jsonify(data=json.loads(session[session_name]))
		total_price = 0.0
		item_names = []
		for item in session:
			if item.endswith("_order"):
				item_names.append(dict(item_name=item[:-6], price=float(session.get(item[:-6] + "_price"))))
				total_price += float(session.get(item[:-6] + "_price"))
		session["total_price"] = total_price
		session["n_orders"] = len(item_names)

		return render_template("cart.html", item_names=item_names)

	@route("/checkout", methods=["POST", "GET"])
	def checkout_view(self):
		if session.get("username"):
			if request.form:
				price = request.form.get("total_price")
				return render_template("checkout.html", price=price)
			else:
				return render_template("checkout.html", price=session.get("total_price"))
		else:
			return redirect(url_for('DashboardView:login_view'))

	@route("/myorder", methods=["POST", "GET"])
	def payment_view(self):
		import controller
		saved_orders = controller.save_orders()
		if saved_orders:
			info = "saved"
		# placed_items = controller.get_orders()
		placed_items = [{item[:-6]:json.loads(session.get(item))} for item in session if item.endswith("_order")]
		# return jsonify(data=placed_items)
		for i in saved_orders:
			session.pop(i, None)
		session.pop("n_orders", None)
		return render_template("myorder.html", data=placed_items, info=info)

	@route("/logout")
	def logout_view(self):
		session.clear()
		return redirect(url_for('DashboardView:home_view'))

	@route("/test/<string:page_alias>")
	def food_test_view(self, page_alias):
		import controller
		food_items = controller.get_food_items()
		food_name = page_alias.replace("_", " ")
		if food_name in food_items:
			ingredients = controller.get_food_data(page_alias)
			data = dict(food_name=food_name, ingredients=ingredients)
			return jsonify(data=data)

	@route("/clear")
	def clear_session(self):
		session.clear()
		return "session cleared"
