from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
import re

class Image(BaseModel):
    user_id = pw.ForeignKeyField(User, backref="images", on_delete="CASCADE")
    image_url = pw.TextField(null=False)

    @hybrid_property
    def full_image_url(self):
        from app import app
        return app.config.get('S3_LOCATION') + self.image_url