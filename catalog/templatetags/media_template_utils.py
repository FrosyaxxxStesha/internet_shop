from django import template


register = template.Library()


@register.filter
def mediapath(obj_image_attr):
    return obj_image_attr.url


@register.simple_tag
def mediapath(obj_image_attr):
    return obj_image_attr.url

