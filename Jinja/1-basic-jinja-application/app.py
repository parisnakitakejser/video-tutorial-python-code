from jinja2 import Template

template = Template('Hello {{ name }}')
template_render = template.render(name='Paris')

print(template_render)