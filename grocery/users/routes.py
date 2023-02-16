from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from grocery import db, bcrypt
from grocery.models import User, Item
from grocery.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetPasswordForm, ResetPasswordForm
from grocery.users.utils import send_reset_email, save_picture

# similar to making an instance of a Flask object (see grocery/__init__.py) : additionally passing in the name of our 'Blueprint': usersappblueprint
usersappblueprint = Blueprint('usersappblueprint', __name__)

@usersappblueprint.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('mainappblueprint.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('usersappblueprint.login'))
    return render_template('register.html', title="Registration", form=form)

@usersappblueprint.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainappblueprint.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You\'ve been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('mainappblueprint.home'))
        else:
            flash('Login Unsuccessful. Plase check email and password', 'danger')
    return render_template('login.html', title="Log In", form=form)


@usersappblueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('mainappblueprint.home'))

@usersappblueprint.route("/account", methods=["POST","GET"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.display_public = form.display_public.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('usersappblueprint.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.display_public.data = current_user.display_public
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form, user=form.username.data)


@usersappblueprint.route("/user/<string:username>")
def user_items(username):
    page = request.args.get('page', 1, type=int)
    userqueried = User.query.filter_by(username=username).first_or_404()
    
    # Can you refactor the home method's query producing 'itemspaginated' specifically how it gets its list of users whose display_pulbic is 'True' all within the Item Table?
    # : users Item.user_id.in_(userstruelist)
    #                   Change userstruelist, to a list of users that have 'display_public' as 'True'
    # 'user', in line 164, is the backref variable to User table while queyring the Item table (see models)
    items = Item.query\
        .filter_by(user=userqueried)\
        .order_by(Item.date_added.desc())\
        .paginate(page=page, per_page=2)
    
    return render_template('user_items.html', items=items, user=userqueried)

# TROUBELSHOOT Routes: Reset_Request, and Reset_Token see if resetting password works with:
#   JWT: https://stackoverflow.com/questions/71292764/which-timed-jsonwebsignature-serializer-replacement-for-itsdangerous-is-better 
#   itsdangerous JSOSerializer: tutorial used 
@usersappblueprint.route("/reset_password", methods=["POST","GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('mainappblueprint.home'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('if user user exists, reset token has been sent','info')
        return redirect(url_for('usersappblueprint.login'))
    return render_template('reset_request.html', title='Reset Pasword', form=form)

@usersappblueprint.route("/reset_password/<token>", methods=["POST","GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('mainappblueprint.home'))
    user = User.verify_reset_token(token)
    if user is None:
            flash('Invalid or expired token','warning')
            return redirect(url_for('usersappblueprint.reset_request'))
    elif user is False:
            flash('That is not working','warning')
            return redirect(url_for('usersappblueprint.reset_request'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You can now log in with new password!', 'success')
        return redirect(url_for('usersappblueprint.login'))
    return render_template('reset_token.html', title='Reset Pasword', form=form)
