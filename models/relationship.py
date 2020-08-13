from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
import re

class Relationship(BaseModel):
    main = pw.ForeignKeyField(User, on_delete='CASCADE')
    follower = pw.ForeignKeyField(User, on_delete='CASCADE')
    is_approved = pw.BooleanField(default=False)
    
    