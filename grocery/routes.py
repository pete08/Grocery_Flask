import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from grocery import app, db, bcrypt
from grocery.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewItem
from grocery.models import User, Item
from flask_login import login_user, logout_user, current_user, login_required

# items = [
#     {
#         'author': 'Peter Hackley',
#         'item_name' : 'item 000',
#         'detail' : 'brand, count, description are all things to describe a list with.',
#         'date_added' : 'April 10, 2023',
#     },
#     {
#         'author': 'Jane Doe',
#         'item_name' : 'item 1',
#         'detail' : 'on a sprign day in May. There is a lorem, Ipsum. Antem Lorem Lorem.',
#         'date_added' : 'April 11, 2023',
#     },
# ]


@app.route("/")
@app.route("/home")
def home():
    userstrue = User.query.filter_by(display_public=True).all()
    userstruelist = []
    for i in userstrue:
        userstruelist.append(i.id)
    page = request.args.get('page', 1, type=int)
    itemspaginated = Item.query.filter(Item.user_id.in_(userstruelist)).paginate(page=page, per_page=2)
    # items = Item.query.order_by(Item.user_id.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', items=itemspaginated)

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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route("/account", methods=["POST","GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

@app.route("/new", methods=['GET', 'POST'])
@login_required
def new_item():
    form = NewItem()
    if form.validate_on_submit():
        post = Item(item_name=form.item_name.data, detail=form.detail.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your item has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('new_item.html', title="New Item", form=form, legend='New Item')

#Consider changing to entire list
@app.route("/item/<int:item_id>")
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', item_name=item.item_name, item=item)

@app.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user != current_user:
        abort(403)
    form = NewItem()
    if form.validate_on_submit():
        item.item_name = form.item_name.data
        item.detail = form.detail.data
        db.session.commit()
        flash('Your item has been updated!', 'success')
        return redirect(url_for('item', item_id=item.id))
    elif request.method == 'GET':
        form.item_name.data = item.item_name
        form.detail.data = item.detail
    return render_template('new_item.html', title="Update Item", form=form, legend='Update Item')

@app.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.user != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted!', 'success')
    return redirect(url_for('home'))


# @app.route("/user/<str:username>")
# def user_items(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     items = Item.query.order_by(Item.user_id.desc()).paginate(page=page, per_page=2)
#     return render_template('home.html', items=items)