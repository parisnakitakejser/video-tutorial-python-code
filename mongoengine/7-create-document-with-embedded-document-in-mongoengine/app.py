from mongoengine import connect
from odm.posts import Posts, PostMetatag, PostCategory

connect(
    db='project1',
    host='localhost',
    port=27017,
    username='mongoadmin',
    password='secret',
    authentication_source='admin'
)

post_metatag = PostMetatag()
post_metatag.title = 'Test meta title'
post_metatag.description = 'meta test description'

post = Posts()
post.title = 'Hello world'
post.url = 'hello-world'
post.content = 'World is nice! :)'
post.metatag = post_metatag
post.status = 'pending'

post_category = PostCategory()
post_category.title = 'category title 1'
post_category.id = '5ea3f1a86f1ab83cc46c8cfc'
post.categorys.append(post_category)

post_category = PostCategory()
post_category.title = 'category title 2'
post_category.id = '5ea3f1e0c43137a34d5dd291'
post.categorys.append(post_category)

post.authors.append('5ea3f21351f65442e5e7383e')
post.authors.append('5ea3f219d65038bc607f70f5')
post.authors.append('5ea3f21e7515c00ee4abaec8')

post.save()