from django import forms
from django.template.defaulttags import register
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def profane_filter_base(dict, check):
    ret_dict = {}
    for key, val in dict.items():
        ret_arr = []
        for err in val:
            if(isinstance(err, forms.ValidationError)):
                if( (err.code == "profane") == check):
                    ret_arr.append(err)
            elif not check:
                ret_arr.append(err)
        if len(ret_arr) > 0:
            ret_dict[key] = ret_arr
    return ret_dict

@register.filter
def profane_filter(dict):
    return profane_filter_base(dict, True)
register.filter('profane_filter', profane_filter)

@register.filter
def normal_filter(dict):
    return profane_filter_base(dict, False)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
@stringfilter
def split(string, sep):
    # https://code.djangoproject.com/ticket/21367
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)
