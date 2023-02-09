from datetime import datetime
from grocery import db, login_manager
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
    items = db.relationship('Item', backref='user', lazy=True)

    # REPR method
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(60), nullable=False, default='')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # REPR method
    def __repr__(self):
        return f"Item('{self.item_name}', '{self.date_added}')"
