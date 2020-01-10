from jinja2 import Template

with open('template/layout.html') as file:
    template = Template(file.read())

print(template.render())