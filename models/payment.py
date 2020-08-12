from models.base_model import BaseModel
import peewee as pw
import re
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from models.user import User
from models.image import Image
from playhouse.hybrid import hybrid_property

class Payment(BaseModel):
    user = pw.ForeignKeyField(User, backref='payments')
    image = pw.ForeignKeyField(Image, backref='payments')
    amount = pw.DecimalField()