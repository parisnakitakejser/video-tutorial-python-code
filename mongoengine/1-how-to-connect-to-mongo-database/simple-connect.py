from mongoengine import connect

# Simple connect just connect as defualt to own mongo host on local machine
connect(db='project1')

# Simple connect point to host and port whitout eny login auth.
connect(db='project1', host='127.0.0.1', port=27017)