from django import template
register = template.Library()

@register.filter
def is_instance(value, class_name):
    return value.__class__.__name__ == class_name

@register.simple_tag
def make_item_seen(value):
    value.is_seen = True
    value.save()
    return ""