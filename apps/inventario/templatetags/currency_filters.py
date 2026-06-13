from django import template

register = template.Library()

@register.filter
def currency(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {formatted}"
