from django import template
from django.utils.safestring import mark_safe

register = template.Library()

INDEX_COLOR = {
    "good": "2a9d8f",
    "moderate": "f4a261",
    "slow": "e76f51",
}

# Green (Good) – 0 to 3.4 seconds 
# Orange (Moderate) – 3.4 to 5.8 seconds 
# Red (Slow) – over 5.8 seconds

INTERACTIVE_COLORS = {
    "good": "2a9d8f",
    "ok": "ffbe0b",
    "long": "f4a261",
    "longer": "e76f51",
}

# Good - nothing to do here = TTI of 2468 milliseconds or less. 
# Ok, but consider improvement = TTI between 2468 and 3280 milliseconds. 
# Longer than recommended = TTI between 3280 and 4500 milliseconds. 
# Much longer than recommended = TTI higher than 4500 milliseconds. 



def to_seconds(value):
    return round(value / 1000, 1)


def to_html(value, color):
    value = to_seconds(value)
    return f'<span style="color:#{ color };">{ value } s</span>'


def color_change(value, data):
    """Cambia el color dependiendo el valor"""
    
    if data == "index":
        if value <= 3400:
             new_value = to_html(value, INDEX_COLOR["good"])
        elif value > 3400 and value <= 5800:
             new_value = to_html(value, INDEX_COLOR["moderate"])
        else:
            new_value = to_html(value, INDEX_COLOR["slow"])

    elif data == "interactive":
        if value <= 2468:
             new_value = to_html(value, INTERACTIVE_COLORS["good"])
        elif value > 2468 and value <= 3280:
             new_value = to_html(value, INTERACTIVE_COLORS["ok"])
        elif value > 3280 and value <= 4500:
             new_value = to_html(value, INTERACTIVE_COLORS["long"])
        else:
            new_value = to_html(value, INTERACTIVE_COLORS["longer"])

    return mark_safe(new_value)


register.filter("colorChange", color_change)
