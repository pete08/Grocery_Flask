from datetime import datetime, timedelta, timezone
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #
import jwt
from grocery import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='dog_0.jpg')
    password = db.Column(db.String(60), nullable=False)
    display_public = db.Column(db.Boolean, nullable=False, default=1)
    items = db.relationship('Item', backref='user', lazy=True)
    
    def get_reset_token(self, expiration=600):
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token

    # @staticmethod
    # def verify_reset_token(token): #
    #     s = Serializer(current_app.config['SECRET_KEY']) #
    #     try: #
    #         user_id = s.loads(token)['user_id'] #
    #     except: #
    #         return None #
    #     return User.query.get(user_id) #
    @staticmethod
    def verify_reset_token(token):
        try:
            # HERE: See what jwt.decode outputs!
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"])
        except:
            return None
        try:
            user_id = data['user_id']
        except:
            return False
        # if data.get('user') != self.id:
        #     return False
        # self.confirmed = True
        # db.session.add(self)
        # return True
        return User.query.get(user_id)
        # return User.query.get(data)

    # REPR method
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}', '{self.display_public}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(20), nullable=False) 
    detail = db.Column(db.String(60), nullable=False, default='')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # REPR method
    def __repr__(self):
        return f"Item('{self.item_name}', '{self.date_added}', '{self.user_id}')"
