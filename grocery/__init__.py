from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# /// -> relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # pass app to bcrypt class to iniitalize bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'usersappblueprint.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from grocery.users.routes import usersappblueprint
from grocery.items.routes import itemsappblueprint
from grocery.main.routes import mainappblueprint

app.register_blueprint(usersappblueprint)
app.register_blueprint(itemsappblueprint)
app.register_blueprint(mainappblueprint)


# initialize DB
# CLI for DB creation: $ python3 <--- does not produce a Flask Application Automatic Context: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts
# CLI for DB creation: $ flask --app grocery shell <--- produces Flask Application Automatice Context: https://flask.palletsprojects.com/en/2.2.x/cli/#open-a-shell. This "Autoamtic Context" is necessary to populate/test DBs
# CLI for recreating DBs: 
#               db.drop_all()
#               db.create_all()
# CLI for applying schema modifications to existing DBs: https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
#### CLI DBs:
#### $ flask --app grocery shell
#### >>> from grocery import db
#### >>> db.create_all()
#### >>> user_1 = User(username='peter', email='p@mail.com, password='password')
#### >>> db.session.add(user_1)
#### >>> db.session.commit()
#### >>> User.query.all()