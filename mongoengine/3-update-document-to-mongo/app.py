from mongoengine import connect
from orm.user import User

connect(
    db='project1',
    host='localhost',
    port=27017,
    username='mongoadmin',
    password='secret',
    authentication_source='admin'
)

# Static params field updater
user = User.objects(email='test@email.com')
user.update(first_name='New Paris', last_name='Nakita Kejser')

# Dynamic params field updater
user2 = User.objects(email='test2@email.com')
fields = {
    'first_name': 'Secound Test',
    'last_name': 'Frist Last Name'
}
user2.update(**fields)

