# Generated by Django 2.2.2 on 2020-11-09 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201109_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='commit_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='down_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='up_num',
            field=models.IntegerField(default=0),
        ),
    ]