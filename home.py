import os
from flask import Flask, render_template
from database import select

app = Flask(__name__)

# Set Flask debug mode if in dev environment
if not int(os.environ['PRODUCTION']):
  app.config['DEBUG'] = True

def post_item(post):
  # Only keep the first line; no newlines please
  post["body"] = post["body"].splitlines()[0]
  return post

def post_main(post):
  # Turn newlines into line breaks
  post["body"] = "<br />".join(post["body"].splitlines())
  return post

@app.route('/')
def home():
  posts = [post_item(post) for post in select("SELECT * FROM posts")]
  return render_template('home.html', posts=posts)

@app.route('/post/<post>')
def post(post):
  posts = select("SELECT * FROM posts WHERE id = %s", (post,))
  if not posts:
    return render_template('error.html', message="Could not find post!")
  post = post_main(posts[0])
  return render_template('post.html', post=post)
