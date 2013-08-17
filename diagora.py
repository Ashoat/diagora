import os
from flask import Flask
from home import home_bp
from post import post_bp

# Register endpoints
app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(post_bp)

# Set Flask debug mode if in dev environment
if not int(os.environ['PRODUCTION']):
  app.config['DEBUG'] = True
