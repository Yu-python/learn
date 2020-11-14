
import os



def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BBS_11_09.settings')



if __name__ == '__main__':
    main()
    import django
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    django.setup()
    from blog import models
    # category_obj = models.Category.objects.filter(blog__user__username='egon').annotate(c=Count('blog__article__id')).values_list('name','c')
    # print(category_obj)

    # tag_obj  = models.Tag.objects.filter(blog__user__username='egon').annotate(c=Count('blog__article__id')).values_list('name','c')
    # print(tag_obj)

    data_obj = models.Article.objects.filter(blog__user__username='egon').annotate(month = TruncMonth('create_time')).values('month').annotate(c=Count('id')).values_list('month','c')
    print(data_obj)