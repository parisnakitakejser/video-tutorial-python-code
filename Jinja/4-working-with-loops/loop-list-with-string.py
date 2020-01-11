import jinja2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))

jinja_var = {
    'users': ['User 1', 'User 2', 'User 3']
}

template = jinja_env.get_template('layout.html')
print(template.render(jinja_var))