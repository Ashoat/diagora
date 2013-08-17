from flask import Blueprint, render_template
from database import select

home_bp = Blueprint('home', __name__)

def parse_post(post):
  # Only keep the first line; no newlines please
  post["body"] = post["body"].splitlines()[0]
  return post

@home_bp.route('/')
def home():
  posts = [parse_post(post) for post in select("SELECT * FROM posts")]
  return render_template('home.html', posts=posts)
