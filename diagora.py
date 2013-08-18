import os
from flask import Flask
from flask_login import LoginManager
import user
from database import close_connection
from home import home_bp
from post import post_bp
from login import login_bp
from compose import compose_bp

app = Flask(__name__)
app.secret_key = user.secret_key

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user.get_user)
login_manager.token_loader(user.load_token)
login_manager.login_view = "login.login"

# Register endpoints
app.register_blueprint(home_bp)
app.register_blueprint(post_bp)
app.register_blueprint(login_bp)
app.register_blueprint(compose_bp)

# Register DB connection teardown
app.teardown_appcontext(close_connection)

# Set Flask debug mode if in dev environment
if not int(os.environ['PRODUCTION']):
  app.config['DEBUG'] = True
