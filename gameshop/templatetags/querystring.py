from django import template

register = template.Library()

@register.simple_tag
def qs_replace(request, **kwargs):
    """
    Повертає поточний querystring, замінюючи/додаючи передані ключі.
    Значення None видаляє ключ із рядка.
    """
    qd = request.GET.copy()

    for k, v in kwargs.items():
        if v in (None, '', []):
            qd.pop(k, None)
        else:
            qd[k] = v

    return qd.urlencode()