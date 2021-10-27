"""
  app.py
  ~~~~~~~~~~~~~~~~~~~~

  The central application.
"""

from flask import (render_template, request, session,
                    url_for, redirect, flash)
from utils.helperfuncs import ( login_valid, username_exists, 
                                add_user )
from utils.decorators import (login_required, admin_login_required)
from init import app, db


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
  if request.method == 'POST':
    query = request.form.get('query')
    results = Food.query.filter(Food.food_name.like(f"%{query}%")).all()
    return render_template('search_results.html', results=results, cnt=len(results))
  return render_template('dashboard.html')


@app.route('/admin')
@login_required
@admin_login_required
def admin():
  return render_template("admin_dashboard.html")


if(__name__ == "__main__"):
  with app.app_context():
    app.run(debug=True)