from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
    'current_category': current_category
    }

@register.inclusion_tag('rango/base.html')
def get_top3_category_list(current_category=None):
    return {
        'categories': Category.objects.order_by('-likes')[:3]
    }