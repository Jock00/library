from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Replace with your email and password
    user = User.query.filter_by(email='alex22@gmail.com').first()
    if user:
        user.is_admin = True
        db.session.commit()
        print("User is now an admin.")
    else:
        print("User not found.")
