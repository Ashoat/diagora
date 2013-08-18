from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user
from user import User
from database import select
from hashlib import sha256
from binascii import unhexlify

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  email = request.form['email']
  users = select("SELECT * FROM users WHERE email = %s", (email,))
  if not users:
    return render_template('error.html', message="Could not find user!")
  password = request.form['password'].encode('ascii')
  salt = unhexlify(users[0]['salt'])
  pw_hash = sha256(password + salt).hexdigest()
  if pw_hash != users[0]['hash']:
    return render_template('error.html', message="Could not find user!")
  login_user(User(users[0]), remember=True)
  return redirect(url_for('home.home'))
