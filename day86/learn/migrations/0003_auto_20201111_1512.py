# Generated by Django 2.2.2 on 2020-11-11 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_book_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]