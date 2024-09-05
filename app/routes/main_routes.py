from flask import Blueprint, render_template
from app.models.books import Books, User
from flask_login import login_required
from app.routes.auth_routes import admin_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    books = Books.query.all()
    return render_template('index.html', books=books)


@main.route('/view_books')
def view_books():
    # Query the User table to get all users
    books = Books.query.all()

    # Render the users in a template
    return render_template('view_books.html', books=books)


@main.route('/view_books_admin')
@login_required
@admin_required
def view_books_admin():
    # Query the User table to get all users
    books = Books.query.all()
    # Render the users in a template
    return render_template('view_books_admin.html', books=books)


@main.route('/view_users')
@login_required
@admin_required
def view_users():
    users = User.query.all()  # Fetch all users from the database
    return render_template('view_users.html', users=users)
