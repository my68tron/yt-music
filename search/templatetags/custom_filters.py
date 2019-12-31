from django import template

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    '''
    This filter cuts all values of arg from the value string
    '''

    return value.replace(arg, '')

# register.filter(cut)