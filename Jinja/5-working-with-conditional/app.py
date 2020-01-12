import jinja2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
jinja_var = {
    'city': 'copenhagen'
}

template = jinja_env.get_template('layout.html')
print(template.render(jinja_var))