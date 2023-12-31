from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# import hmac
# str_to_bytes = lambda s: s.encode("utf-8") if isinstance(s, str) else s
# safe_str_cmp = lambda a, b: hmac.compare_digest(str_to_bytes(a), str_to_bytes(b))
# import hmac

# def safe_str_cmp(a: str, b: str) -> bool:
#     """This function compares strings in somewhat constant time. This
#     requires that the length of at least one string is known in advance.

#     Returns `True` if the two strings are equal, or `False` if they are not.
#     """

#     if isinstance(a, str):
#         a = a.encode("utf-8")  # type: ignore

#     if isinstance(b, str):
#         b = b.encode("utf-8")  # type: ignore

#     return hmac.compare_digest(a, b)
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '') 
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150), nullable = False)
    model = db.Column(db.String(200))
    year = db.Column(db.String(20))
    color = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,make,model,year,color,user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.user_token = user_token


    def __repr__(self):
        return f'The following car has been added to the inventory: {self.make}, {self.model}'

    def set_id(self):
        return (secrets.token_urlsafe())

class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make','model','year', 'color']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)