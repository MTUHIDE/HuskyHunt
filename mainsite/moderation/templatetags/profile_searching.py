from django import template

register = template.Library()

@register.filter
def getPFPFromUserDict(value, index):
    try:
        return value[index].picture.url
    except ValueError:
        return "https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg"
    except KeyError:
    	return "https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg"


@register.filter
def getPointsFromUserDict(value, index):
    return value[index].points

@register.filter
def getFlagsFromUserDict(value, index):
    return value[index].flags_today