from django import template
from decimal import *

register = template.Library()

@register.filter
def multiply(value, arg):
    value = Decimal(value) * Decimal(arg)
    return round(value, 2)