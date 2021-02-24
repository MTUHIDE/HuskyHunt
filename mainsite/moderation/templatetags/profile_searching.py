from django import template

register = template.Library()

@register.filter
def getPFPFromUserDict(value, index):
    return value[index].picture.url

@register.filter
def getPointsFromUserDict(value, index):
    return value[index].points

@register.filter
def getFlagsFromUserDict(value, index):
    return value[index].flags_today