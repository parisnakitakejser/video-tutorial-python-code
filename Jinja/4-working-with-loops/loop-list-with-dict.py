import jinja2

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))

jinja_var = {
    'employes': [{
        'name': 'Paris',
        'office': 'Denmark'
    }, {
        'name': 'Bob',
        'office': 'Germany'
    }]
}

template = jinja_env.get_template('layout2.html')
print(template.render(jinja_var))