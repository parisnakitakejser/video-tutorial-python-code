from mongoengine import connect
from mongoengine.errors import NotUniqueError
from orm.user import User

connect(
    db='project1',
    host='localhost',
    port=27017,
    username='mongoadmin',
    password='secret',
    authentication_source='admin'
)

try:
    user = User(email='test@email.com')
    user.first_name = 'Paris'
    user.last_name = 'Nakita Kejser'
    user.save()
except NotUniqueError as e:
    print('E-mail allready found')