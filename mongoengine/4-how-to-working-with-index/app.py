from mongoengine import connect
from odm.posts import Posts

connect(
    db='project1',
    host='localhost',
    port=27017,
    username='mongoadmin',
    password='secret',
    authentication_source='admin'
)

post = Posts()
post.title = 'Hello world'
post.url = 'hello-world'
post.content = 'World is nice! :)'
post.status = 'pending'
post.save()