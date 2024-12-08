from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Access dictionary keys dynamically."""
    return dictionary.get(key, {})
