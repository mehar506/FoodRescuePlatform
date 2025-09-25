from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm, FoodPostForm
from app.models import User, FoodPost
from app import db
from flask import Blueprint

main = Blueprint('main', __name__)  # Blueprint

# Home
@main.route('/')
def home():
    return "<h1>🍲 Welcome to Food Rescue Platform!</h1>"

# Register
@main.route("/register", methods=["GET", "POST"])
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

        if form.role.data == 'organization':
            flash("✅ Registration successful! Your account is pending admin approval.", "warning")
        else:
            flash("✅ Account created successfully! You can now log in.", "success")

        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Login
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if user.check_password(form.password.data):
                # Block unverified organizations
                if user.role == 'organization' and not user.is_verified:
                    flash("⚠️ Your account is pending admin approval. Please wait until verification.", "warning")
                    return redirect(url_for("main.login"))

                login_user(user)
                flash("🎉 Login successful!", "success")
                return redirect(url_for("main.dashboard"))
            else:
                flash("❌ Invalid password", "danger")
        else:
            flash("❌ No account found with that email.", "danger")

    return render_template("login.html", form=form)

# Logout
@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 You have been logged out.", "info")
    return redirect(url_for("main.login"))

# Dashboard
@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# Create food post (for restaurants only)
@main.route("/food/new", methods=["GET", "POST"])
@login_required
def new_food_post():
    if current_user.role != 'restaurant':
        flash("Only restaurants can post food.", "danger")
        return redirect(url_for('main.dashboard'))

    form = FoodPostForm()
    if form.validate_on_submit():
        post = FoodPost(
            title=form.title.data,
            description=form.description.data,
            quantity=form.quantity.data,
            pickup_time=form.pickup_time.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash("✅ Food post created successfully!", "success")
        return redirect(url_for('main.dashboard'))

    return render_template("new_food_post.html", form=form)

# View all available food posts (for organizations)
@main.route("/food/posts")
@login_required
def view_food_posts():
    if current_user.role != 'organization':
        flash("Only organizations can view available food posts.", "danger")
        return redirect(url_for('main.dashboard'))

    posts = FoodPost.query.filter_by(status="available").all()
    return render_template("food_posts.html", posts=posts)

# Admin dashboard
@main.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

# Verify an organization
@main.route("/admin/verify/<int:user_id>")
@login_required
def verify_user(user_id):
    if current_user.role != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    user = User.query.get(user_id)
    if user and user.role == 'organization':
        user.is_verified = True
        db.session.commit()
        flash(f"✅ {user.name} has been verified!", "success")
    return redirect(url_for("main.admin_dashboard"))
