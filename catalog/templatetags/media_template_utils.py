from django import template


register = template.Library()


@register.filter
def mediapath(obj_image_attr):
    return obj_image_attr.url


@register.simple_tag
def mediapath(obj_image_attr):
    return obj_image_attr.url


@register.filter
def current(versions):
    if not versions:
        return None

    for version in versions:
        if version.current:
            return version


