from flask import render_template, url_for, flash, redirect
from grocery import app
from grocery.forms import RegistrationForm, LoginForm
from grocery.models import User, Item

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Registration", form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You\'ve been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Plase check suername and apssword', 'danger')
    return render_template('login.html', title="Log In", form=form)