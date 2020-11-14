# Generated by Django 2.2.2 on 2020-11-09 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201109_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name_plural': '文章详情'},
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name': '博客', 'verbose_name_plural': '博客'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '分类'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': '评论'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '标签'},
        ),
        migrations.AlterModelOptions(
            name='upanddown',
            options={'verbose_name_plural': '点赞'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '用户'},
        ),
        migrations.AlterField(
            model_name='upanddown',
            name='id_down',
            field=models.BooleanField(null=True),
        ),
    ]
