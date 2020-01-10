import jinja2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
template = jinja_env.get_template('layout.html')

print(template.render())