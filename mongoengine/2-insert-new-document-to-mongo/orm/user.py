from mongoengine import Document, StringField, EmailField


class User(Document):
    email = EmailField(required=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)