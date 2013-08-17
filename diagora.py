import os
from flask import Flask
from database import get_db

app = Flask(__name__)

# Set Flask debug mode if in dev environment
if not int(os.environ["PRODUCTION"]):
  app.config['DEBUG'] = True

@app.route('/')
def diagora():
  d = get_db()
  return 'Hello World!'
