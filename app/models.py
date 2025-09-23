from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User loader (for Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "restaurant" or "organization"

    # Extra fields
    name = db.Column(db.String(150), nullable=False)   # Restaurant or Org Name
    address = db.Column(db.String(250), nullable=True)
    registration_number = db.Column(db.String(100), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

    food_posts = db.relationship('FoodPost', backref='restaurant', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class FoodPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.String(50), nullable=False)
    pickup_time = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="available")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
