from django import template
from app.models import tbl_category_desc

register = template.Library()

@register.simple_tag
def get_obj(pk, attr):
    obj = getattr(tbl_category_desc.objects.get(pk=int(pk)), attr)
    return obj