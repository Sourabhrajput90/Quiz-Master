from django import template

register = template.Library()

@register.filter
def times_100(value):
    """Multiplies the given value by 100"""
    try:
        return int(value) * 100
    except (ValueError, TypeError):
        return 0  # Return 0 if value is invalid
