import lib.settings
from odm.posts import Posts
from odm.users import Users

post = Posts()
post.title = 'test post title'
post.description = 'description for this test post here!'
post.save()

user = Users()
user.name = 'Paris Nakita Kejser'
user.save()