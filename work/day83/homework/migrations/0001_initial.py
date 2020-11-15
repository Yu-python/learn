# Generated by Django 2.2.2 on 2020-11-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(help_text='id', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='标题', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, help_text='价格', max_digits=5)),
                ('publish', models.CharField(help_text='出版社', max_length=255)),
            ],
        ),
    ]