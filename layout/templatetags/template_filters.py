from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter(name='space_to_dash')
@stringfilter
def space_to_dash(value):
    result =value.replace(" ", "-")
    return result

@register.simple_tag()
def debug_object_dump(var):
    return vars(var)