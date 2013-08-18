from flask import Blueprint, render_template
from flask_login import current_user
from database import select

post_bp = Blueprint('post', __name__)

def parse_post(post):
  # Turn newlines into line breaks
  post["body"] = "<br />".join(post["body"].splitlines())
  return post

@post_bp.route('/post/<post>')
def post(post):
  posts = select(
    'SELECT p.*, u.name FROM posts p '
    'LEFT JOIN users u ON u.id = p.user '
    'WHERE p.id = %s',
    (post,)
  )
  if not posts:
    return render_template(
      'error.html',
      message="Could not find post!",
      user=current_user,
    )
  topics = select(
    'SELECT "to"."name" FROM tags ta '
    'LEFT JOIN topics "to" ON "to"."id" = ta.to '
    'WHERE ta.from = %s',
    (posts[0]["id"],)
  )
  topics = [topic["name"] for topic in topics]
  post = parse_post(posts[0])
  return render_template(
    'post.html',
    post=post,
    user=current_user,
    topics=topics,
  )
