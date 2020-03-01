from datetime import date
from vlabs import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_account(account_id):
    return Account.query.get(int(account_id))

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    labs = db.relationship('Lab', backref='author', lazy=True)

    def __repr__(self):
        return f'Account details : {self.email} {self.labs}'

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    stream = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    lab_url = db.Column(db.String(80), nullable=False, default='demo-lab.html')
    date_posted = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    
    def __repr__(self):
        return f'Lab details : {self.title} posted on {self.date_posted}'