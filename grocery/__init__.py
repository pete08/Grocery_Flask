from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from grocery.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt() # pass app to bcrypt class to initialize bcrypt
login_manager = LoginManager()
login_manager.login_view = 'usersappblueprint.login'
login_manager.login_message_category = 'info'

mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from grocery.users.routes import usersappblueprint
    from grocery.items.routes import itemsappblueprint
    from grocery.main.routes import mainappblueprint
    from grocery.errors.handlers import errorappblueprint
    app.register_blueprint(usersappblueprint)
    app.register_blueprint(itemsappblueprint)
    app.register_blueprint(mainappblueprint)
    app.register_blueprint(errorappblueprint)

    return app


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