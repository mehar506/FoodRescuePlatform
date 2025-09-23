from flask import render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from app.forms import RegistrationForm
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "<h1>🍲 Welcome to Food Rescue Platform!</h1>"

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            name=form.name.data,
            address=form.address.data,
            registration_number=form.registration_number.data if form.role.data == 'organization' else None,
            is_verified=False if form.role.data == 'organization' else True
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("✅ Account created successfully! Pending verification if you are an organization.", "success")
        return redirect(url_for('main.home'))

    # 👇 This is what loads your register.html
    return render_template('register.html', form=form)
