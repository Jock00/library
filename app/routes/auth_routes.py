from flask import render_template, redirect, url_for, flash, Blueprint, \
    render_template, request, session
from app.forms.book_forms import BookForm, RegisterForm, LoginForm, EditBookForm
from app import db
from app.models.books import User, Books
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

auth = Blueprint('auth', __name__)


@auth.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Create a new book entry
        new_book = Books(
            name=form.name.data,
            author=form.author.data,
            image=form.image.data,
            description=form.description.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('main.view_books'))
    return render_template('add_book.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if the user already exists by email or username
        existing_user = User.query.filter(User.email == form.email.data).first()
        if existing_user:
            flash(
                'User already exists with this email or username. Please log in or choose a different one.',
                'danger')
            return redirect(url_for('auth.register'))

        # Hash the password with the correct method
        hashed_password = generate_password_hash(form.password.data,
                                                 method='pbkdf2:sha256',
                                                 salt_length=8)

        # Create a new User instance
        new_user = User(
            username=form.email.data.split("@")[0],
            email=form.email.data,
            password_hash=hashed_password
        )

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()

            # Store the user ID in the session to keep the user logged in
            session['user_id'] = new_user.id
            flash('Account created successfully! You are now logged in.',
                  'success')

            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error: Unable to register the user. Try again.', 'danger')

    return render_template('register.html', form=form)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You must be an admin to view this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)

    return decorated_function


### BOOKS
# @auth.route('/edit-book/<int:book_id>', methods=['POST'])
# @login_required
# @admin_required
# def edit_book(book_id):
#     book = Books.query.get_or_404(book_id)
#     if request.form.get('action') == 'Edit':
#         return redirect(url_for('main.edit_book_form', book_id=book.id))
#     elif request.form.get('action') == 'Delete':
#         db.session.delete(book)
#         db.session.commit()
#         flash('Book deleted successfully!', 'success')
#         return redirect(url_for('main.view_books'))


# @auth.route('/edit-book-form/<int:book_id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_book_form(book_id):
#     book = Books.query.get_or_404(book_id)
#     form = EditBookForm(obj=book)
#     if form.validate_on_submit():
#         book.name = form.name.data
#         book.author = form.author.data
#         book.image = form.image.data
#         book.description = form.description.data
#         db.session.commit()
#         flash('Book updated successfully!', 'success')
#         return redirect(url_for('main.view_books'))
#     return render_template('edit_book_form.html', form=form, book=book)


@auth.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    book = Books.query.get_or_404(book_id)
    form = EditBookForm(obj=book)
    if form.validate_on_submit():
        book.name = form.name.data
        book.author = form.author.data
        book.image = form.image.data
        book.description = form.description.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('main.view_books'))
    return render_template('edit_book_form.html', form=form, book=book)


@auth.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    book = Books.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('main.view_books'))
