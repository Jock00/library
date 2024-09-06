from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'))  # User who posted the book

    comments = db.relationship('Comment', backref='book', lazy=True)
    reviews = db.relationship('Reviews', backref='book', lazy=True)
    user = db.relationship('User', backref='books_added', lazy=True)

    def __repr__(self):
        return f"Books(id={self.id}, name='{self.name}', author='{self.author}')"


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Relationship to Users
    user = db.relationship('User', backref='user_reviews', lazy=True)

    def __repr__(self):
        return f"Reviews(id={self.id}, content='{self.content[:30]}...', rating={self.rating})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship to Reviews
    reviews = db.relationship('Reviews', backref='review_user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    user = db.relationship('User', backref='comments')
