from django import template
from rango.models import Category, Course

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

@register.inclusion_tag('rango/course_list.html')
def get_course_list():
    return {
        'course_list': Course.objects.all(),
    }