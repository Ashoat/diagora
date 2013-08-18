from flask import Blueprint, render_template
from flask_login import current_user
from database import select
from bs4 import BeautifulSoup

home_bp = Blueprint('home', __name__)

def parse_post(post):
  # Only keep the first line; no newlines please
  soup = BeautifulSoup(post["body"])
  for tag in soup.findAll(True):
    tag.hidden = True
  post["body"] = soup.renderContents()
  return post

@home_bp.route('/')
def home():
  posts = select(
    "SELECT p.*, u.name FROM posts p LEFT JOIN users u ON u.id = p.user"
  )
  parsed = [parse_post(post) for post in posts]
  return render_template(
    'home.html',
    posts=parsed,
    user=current_user,
  )
