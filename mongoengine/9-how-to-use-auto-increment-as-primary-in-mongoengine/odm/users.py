from mongoengine import Document, StringField, DateTimeField, SequenceField
from datetime import datetime


class Users(Document):
    user_id = SequenceField(primary_key=True)

    name = StringField()

    created_at = DateTimeField(default=datetime.utcnow)