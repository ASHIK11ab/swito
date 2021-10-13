from flask import (Flask, render_template, request, session,
                    url_for, redirect, flash)
from utils.helperfuncs import ( login_valid, get_category_of_user,
                              username_exists, add_user )
from init import app, db
from models import *
from mydecorators import *
from sqlalchemy import and_
from sqlalchemy.orm import aliased


@app.route('/')
def index():
  return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    # Flash error incase of invalid credentials
    if not login_valid(username, password):
      flash('Invalid username or password', 'danger')
      return redirect(request.url)

    session["user"] = username
    if username == 'Admin':
      return redirect('/admin')

    session["category"] = get_category_of_user(username)
    return redirect('/dashboard')

  return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')

  username = request.form.get('username')
  password = request.form.get('password')
  confirm_password = request.form.get('confirm_password')

  if password != confirm_password:
    flash('Passwords dont match', 'danger')
    return redirect(request.url)

  # Flash a error if username is aldready taken.
  if username_exists(username):
    flash('Username aldready exists', 'danger')
    return redirect(request.url)

  add_user(username, password)

  session["user"] = username
  if username == 'admin':
    return redirect('/admin')
  session["category"] = get_category_of_user(username)

  return redirect('/dashboard')


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
  if request.method == 'POST':
    query = request.form.get('query')
    results = Food.query.filter(Food.food_name.like(f"%{query}%")).all()
    return render_template('search_results.html', results=results, cnt=len(results))
  return render_template('dashboard.html')

@app.route('/Place-order/<int:order_id>')
@login_required
def place_order(order_id):
  food = Food.query.get(order_id)
  if food is None:
    return "<h1>Invalid food id</h1>"
  food.addOrder(username = session["user"])
  flash("Order placed")
  return redirect(url_for("dashboard"))

@app.route('/logout')
@login_required
def logout():
  session.clear()
  return redirect(url_for('login'))

@app.route('/admin')
@login_required
@admin_login_required
def admin():
  return render_template("admin_dashboard.html")

@app.route('/Admin/All-customers')
@login_required
@admin_login_required
def all_customers():
  c = aliased(Customer)
  p = aliased(Purchase)
  customers = Customer.query.with_entities(c.id, c.cust_name, c.phone, p.p_cnt, p.category).filter(c.id == p.id).all()
  return render_template("all_customers.html", customers=customers, cnt=len(customers))

@app.route('/Admin/add-item', methods=["GET", "POST"])
@login_required
@admin_login_required
def add_item():
  if request.method == 'POST':
    food_name = request.form.get('food_name')
    food_name = food_name.capitalize()
    cost = int(request.form.get('cost'))
    food = Food(food_name=food_name, cost=cost)
    db.session.add(food)
    db.session.commit()
    flash("Food added successfully", "success")
    return redirect(request.url)
  else: 
    return render_template('add_item.html')

@app.route('/Admin/All-orders')
@login_required
@admin_login_required
def all_orders():
  orders = Order.query.with_entities(Order.id).all()
  return render_template("all_orders.html", orders=orders)

@app.route('/Admin/order/<int:order_id>')
@login_required
@admin_login_required
def order(order_id):
  c = aliased(Customer)
  f = aliased(Food)
  order = Customer.query.with_entities(c.cust_name, o.id, f.id, f.food_name, f.cost).filter(o.id == order_id).first()
  return render_template("order.html", order=order)

@app.route('/Admin/All-items')
@login_required
@admin_login_required
def all_items():
  items = Food.query.all()
  return render_template("all_items.html", items=items)

if(__name__ == "__main__"):
  with app.app_context():
    app.run(debug=True)