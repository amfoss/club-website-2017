from django.template import Library
from django.template.defaultfilters import stringfilter
import json
from django.utils.safestring import mark_safe

register = Library()

@register.filter(is_safe=True)
def jsonify(string):
    return mark_safe(simplejson.loads(string))

@register.filter(name='addcss')
def addcss(field, css):
       return field.as_widget(attrs={"class":css})
