from django import template
from django.http import HttpRequest

register = template.Library()

@register.simple_tag(takes_context=True)
def my_capitalize(context: str, text:str):
    try:

        return str(text).capitalize()
    except Exception as error:
        return f"ERROR WITH SIMPLE TAG my_capitalize  __{1, error}__"

@register.filter(name="my_slice")
def mySlice(source: str, length: int):
    return source[:length]




