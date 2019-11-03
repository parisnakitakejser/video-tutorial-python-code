from configparser import ConfigParser

config = ConfigParser()

config['DEFAULT'] = {
    'title': 'Hello world',
    'compression': 'yes',
    'compression_level': '9'
}

config['database'] = {}
database = config['database']
database['host'] = '127.0.0.1'
database['user'] = 'username'
database['pass'] = 'password'
database['keep-alive'] = 'no'

with open('config.ini', 'w') as configfile:
    config.write(configfile)