from django import template
from decimal import *

register = template.Library()

@register.filter
def tofloat(value):
	return float(value)
    