from django import template

register = template.Library()


@register.filter()
def split_tags(value, delimiter="|"):
    if value == '[None]':
        return None
    return value.split(delimiter)


@register.filter()
def format_views(num):
    if num >= 1000000:
        return str(num // 1000000) + 'M'
    elif num >= 1000:
        return str(num // 1000) + 'k'
    else:
        return str(num)


@register.filter()
def percentify(num):
    try:
        num = float(num)
    except:
        return num
    return f'{round(num * 100, 2)}%'
