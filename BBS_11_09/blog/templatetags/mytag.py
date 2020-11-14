from django.template import library

register = library.Library()
from .. import models
from django.db.models import Count
from django.db.models.functions import TruncMonth


@register.inclusion_tag('left-index.html')
def left(username):
    category_obj = models.Category.objects.filter(blog__user__username=username).annotate(
        c=Count('blog__article__id')).values_list('name', 'c')
    tag_obj = models.Tag.objects.filter(blog__user__username=username).annotate(
        c=Count('blog__article__id')).values_list(
        'name', 'c')
    data_obj = models.Article.objects.filter(blog__user__username=username).annotate(
        month=TruncMonth('create_time')).values('month').annotate(c=Count('id')).values_list('month', 'c')

    return {'category_obj': category_obj, 'tag_obj': tag_obj, 'data_obj': data_obj,'username':username}
