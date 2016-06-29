from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    accounts = db.relationship('Account', backref = 'author', lazy = 'dynamic')
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)  

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    account_name = db.Column(db.String(140))
    counter_id = db.Column(db.Integer)
    goal_id = db.Column(db.Integer)
    token = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Account %r>' % (self.account_name)