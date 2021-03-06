"""
  app.py
  ~~~~~~~~~~~~~~~~~~~~

  The central application.
"""

from flask import (render_template, request, session, render_template_string,
                    url_for, redirect, flash, make_response, jsonify)
from utils.helperfuncs import *
from utils.gdriveupload import upload_file
from utils.decorators import (login_required, admin_login_required)
from init import create_app

app = create_app()

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
    if username == 'admin':
      return redirect('/admin')

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

  return redirect('/dashboard')


@app.route('/logout')
@login_required
def logout():
  session.clear()
  return redirect(url_for('login'))


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
  foods, tags = get_dashboard_foods()
  return render_template('dashboard.html', foods=foods, tags=tags)


@app.route('/dashboard/foods/<int:food_id>')
@login_required
def get_food_details(food_id):
  if request.args.get('request-type') == 'similar-foods':
    similar_foods = get_similar_foods(food_id)
    return make_response(jsonify(similar_foods), 200) 
  else:
    food, tags = get_food_info(food_id)
    if food is None:
      return render_template_string(
        """
          <h1>Invalid URL</h1>
          <h2>Redirecting to Dashboard</h2>
          <script>
            setTimeout(() => window.location = `${window.origin}/dashboard`, 3000);
          </script>
        """)
    return render_template('food.html', food=food, tags=tags)


@app.route('/dashboard/cart')
@login_required
def user_cart():
  items = db.session.query(Food, Cart, User)\
          .with_entities(Food.id, Food.name, Food.price, Cart.quantity)\
          .filter(
            Food.id == Cart.food_id, User.id == Cart.user_id,
            User.username == 'user1'
          ).all()

  results = []
  for row in items:
    result = {}
    for column in row.keys():
      result[column] = row[column]
    results.append(result)

  return make_response(jsonify(results), 200)


@app.route('/dashboard/cart/add', methods=["POST"])
@login_required
def add_food_to_cart():
  food_id = int(request.form['food-id'])
  quantity = int(request.form['quantity'])

  (status, msg) = can_add_item_to_cart(food_id, quantity, session['user'])

  if not status:
    return make_response(jsonify({'msg': msg, 'status': 'failure'}), 404)

  user = get_user(session['user'])
  user.add_item_to_cart(food_id, quantity)
  return make_response(jsonify({
    'msg': msg,
    'status': 'success'
  }), 200)


@app.route('/dashboard/orders/new', methods=["POST"])
@login_required
def place_order():
  food_id = int(request.form['food-id'])
  quantity = int(request.form['quantity'])

  food, tags = get_food_info(food_id)

  if food is None:
    return make_response(jsonify({
      'msg': 'Invalid food id',
      'status': 'failure'
    }), 404)

  if food.quantity == 0:
    return make_response(jsonify({
      'msg': 'Food out of stock',
      'status': 'failure'
    }), 404)
  
  if quantity > food.quantity:
    return make_response(jsonify({
      'msg': 'Enter lesser quantity',
      'status': 'failure'
    }), 404)

  user = get_user(session['user'])
  date = get_current_date()
  time = get_current_time()

  user.place_order(food, quantity, date=date, time=time)
  return make_response(jsonify({
    'msg': 'Order placed successfully',
    'status': 'success'
  }), 200)


@app.route('/admin')
@login_required
@admin_login_required
def admin():
  return render_template('admin_dashboard.html')


@app.route('/admin/foods')
@login_required
@admin_login_required
def manage_foods():
  tags = get_tags()
  return render_template('products.html', tags=tags)


@app.route('/admin/foods/add', methods=["POST"])
@login_required
@admin_login_required
def add_food():
  if not 'image' in request.files:
    resp = {
      "msg": "File part missing",
      "status": "failure"
    }
    return make_response(jsonify(resp), 404)
  
  # Get form data.
  name = request.form['name']
  price = request.form['price']
  quantity = request.form['quantity']
  tags = request.form['tags'].split(',')
  image_file = request.files.get('image')

  if valid_extension(image_file.filename):
    upload_successfull, img_url = upload_file(image_file, category="FOODS")
    # When upload to storage fails.
    if not upload_successfull:
      resp = { "msg": "Unable to upload file", "status": "failure" }
      status_code = 404
    else:
      add_food_to_db(name, price, quantity, img_url, tags)
      resp = { "msg": "Food added successfully", "status": "success" }
      status_code = 200
  else:
    resp = { "msg": "File type not supported", "status": "failure" }
    status_code = 404

  return make_response(jsonify(resp), status_code)


@app.route('/admin/foods/tags')
@login_required
@admin_login_required
def manage_tags():
  tags = get_tags()
  return render_template('food-tags.html', tags=tags, tags_cnt=len(tags))


@app.route('/admin/foods/tags/add', methods=["POST"])
@login_required
@admin_login_required
def add_tag():
  tag = request.form.get('name')
  # Add tag to database if not aldready exists.
  if food_tag_exists(tag):
    msg = "Tag name not available"
    status = "failure"
    status_code = 404
  else:
    create_food_tag(tag)
    msg = "Tag created successfully"
    status = "success"
    status_code = 200
  return make_response(jsonify({"msg": msg, "status": status}), status_code)


if(__name__ == "__main__"):
  with app.app_context():
    app.run()