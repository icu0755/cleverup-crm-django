from django import template
from django.utils.safestring import mark_safe

__author__ = 'Pixel'

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_customer_item(dictionary, key):
    return dictionary.get('customer_%s' % key.id)


@register.filter()
def presence(was_present):
    if was_present:
        return mark_safe('<span class="glyphicon glyphicon-ok"></span>')
    return mark_safe('<span class="glyphicon glyphicon-remove"></span>')
