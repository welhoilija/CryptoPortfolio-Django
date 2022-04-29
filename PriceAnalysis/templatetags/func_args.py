from django import template

register = template.Library()

@register.simple_tag
def func_args(holding, days):
    return holding.calculate_PL(days)