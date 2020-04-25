from mongoengine import connect
from odm.posts import Posts, PostCategory

connect(
    db='project1',
    host='localhost',
    port=27017,
    username='mongoadmin',
    password='secret',
    authentication_source='admin'
)

post = Posts.objects.get(pk="5ea3f264290e1c5733baa7b7")

cat_inx = 1

post_category = PostCategory()
post_category.id = '5ea3f6cd34d222091bdae306'
post_category.title = 'new push category title here'

update_dict = {
    'set__metatag__title': 'new title changed',  # $set.metatag.title
    f'set__categorys__{cat_inx}__title': 'new category title',  # $set.categorys.0.title
    'push__authors': '5ea3f641e5e3bdda84df7269',  # $push.authors
}
post.update(**update_dict)

update_dict = {
    'push__categorys': post_category,  # $push.categorys
}
post.update(**update_dict)

post.authors.pop(2)

post.save()