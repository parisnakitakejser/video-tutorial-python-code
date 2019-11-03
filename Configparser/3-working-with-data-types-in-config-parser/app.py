from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

title = config.get('DEFAULT', 'title')
print('title', type(title), title)

username = config.get('database', 'user')
port = config.getint('database', 'port')
keep_alive = config.getboolean('database', 'keep-alive')
timeout = config.getint('database', 'timeout', fallback=60)

print('user', type(username), username)
print('port', type(port), port)
print('keep_alive', type(keep_alive), keep_alive)

print('timeout', type(timeout), timeout)