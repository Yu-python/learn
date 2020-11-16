# Generated by Django 2.2.2 on 2020-11-16 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('addr', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('publish', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='learn.Publish')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_delete', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=255)),
                ('book', models.ManyToManyField(db_constraint=False, related_name='books', to='learn.Book')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]