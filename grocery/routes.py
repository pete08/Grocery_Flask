from flask import render_template, url_for, flash, redirect, request
from grocery import app, db, bcrypt
from grocery.forms import RegistrationForm, LoginForm
from grocery.models import User, Item
from flask_login import login_user, logout_user, current_user, login_required

store_items = [
    {
        'author': 'Peter Hackley',
        'item_name' : 'needed item',
        'detail' : 'brand, count, description',
        'date_added' : 'April 10, 2023',
    },
    {
        'author': 'Jane Doe',
        'item_name' : 'Needed Item 2',
        'detail' : 'Name Brand, x2',
        'date_added' : 'April 11, 2023',
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', store_items = store_items)

@app.route("/about")
def about():
    return render_template('about.html', title="About Page")

@app.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Registration", form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You\'ve been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Plase check email and password', 'danger')
    return render_template('login.html', title="Log In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")
