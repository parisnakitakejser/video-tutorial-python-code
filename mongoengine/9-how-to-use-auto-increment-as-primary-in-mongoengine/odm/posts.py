from mongoengine import Document, StringField, DateTimeField, SequenceField
from datetime import datetime


class Posts(Document):
    post_id = SequenceField()

    title = StringField()
    description = StringField()

    created_at = DateTimeField(default=datetime.utcnow)
