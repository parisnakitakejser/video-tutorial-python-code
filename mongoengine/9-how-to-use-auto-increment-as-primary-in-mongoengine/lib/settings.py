from mongoengine import connect

connect(
    db='test',
    host='localhost',
    port=27017,
    username='mongoadmin',
    password='secret',
    authentication_source='admin'
)