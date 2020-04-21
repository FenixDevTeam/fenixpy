from main import app
from flask import request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime



db = SQLAlchemy(app)
ma = Marshmallow(app)

class Stats(db.Model):
    
    __tablename__ = 'plan_users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uuid = db.Column(db.String(36), nullable=False)
    registered = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(16), nullable=False)
    times_kicked = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Player {self.name}>'
    

    @staticmethod
    def get_all():
        page = request.args.get('page', 1, type=int)
        players = Stats.query.paginate(page=page, per_page=20)
        return players

    @staticmethod
    def get_by_name(name):
        stats = Stats.query.filter_by(name=name).first()
        return stats

class User(db.Model, UserMixin):
    
    __tablename__ = 'fx_users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    uuid =  db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    des = db.Column(db.Text, nullable=True)
    Fstaff = db.Column(db.Integer, default=0, nullable=False)
    isBan = db.Column(db.Integer, default=0, nullable=False)
    last_seen = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()