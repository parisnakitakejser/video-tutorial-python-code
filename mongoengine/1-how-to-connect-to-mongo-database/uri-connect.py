from mongoengine import connect

connect(db='test', host='mongodb://mongoadmin:secret@localhost/project1')