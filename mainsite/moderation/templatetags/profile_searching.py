from django import template

register = template.Library()

@register.filter
def getPFPFromDict(value, index):
    return value[index].picture.url