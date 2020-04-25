from mongoengine import Document, StringField, DictField, ListField, DateTimeField


class Posts(Document):
    title = StringField(db_field='blog-title-test')
    url = StringField()
    content = StringField()
    metatag = DictField()
    categorys = ListField()
    authors = ListField()
    status = StringField()
    updated_at = DateTimeField()
    created_at = DateTimeField()

    meta = {
        'collection': 'custom-post-collection',
        'auto_create_index': True,
        'index_background': True,
        'indexes': [{
            'name': 'status',
            'fields': ('status', 'created_at', )
        }, {
            'name': 'url',
            'fields': ('url', ),
            'unique': True
        }]
    }