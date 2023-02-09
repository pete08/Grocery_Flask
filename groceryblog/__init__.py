from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# /// -> relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # pass app to bcrypt class to iniitalize bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from groceryblog import routes


# initialize DB
# CLI for DB creation: $ python3 <--- does not produce a Flask Application Automatic Context: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts
# CLI for DB creation: $ flask --app grocery shell <--- produces Flask Application Automatice Context: https://flask.palletsprojects.com/en/2.2.x/cli/#open-a-shell. This "Autoamtic Context" is necessary to populate/test DBs
#### CLI DBs:
#### $ flask --app grocery shell
#### >>> from grocery import db
#### >>> db.create_all()
#### >>> user_1 = User(username='peter', email='p@mail.com, password='password')
#### >>> db.session.add(user_1)
#### >>> db.session.commit()
#### >>> User.query.all()