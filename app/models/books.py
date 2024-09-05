from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    # Relationship to Reviews
    reviews = db.relationship('Reviews', backref='book', lazy=True)

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
    # Updated the backref name to avoid conflict
    reviews = db.relationship('Reviews', backref='review_user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"
