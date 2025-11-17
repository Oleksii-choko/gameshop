from django import template

register = template.Library()

@register.simple_tag
def qs_replace(request, **kwargs):
    """
    Повертає поточний querystring, замінюючи/додаючи передані ключі.
    Значення None видаляє ключ із рядка.
    """
    query = request.GET.copy()
    for k, v in kwargs.items():
        if v is None:
            query.pop(k, None)
        else:
            query[k] = v
    return query.urlencode()