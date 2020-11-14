from django.db import models

# Create your models here.


class User(models.Model):
    choices = ((1,'super_vip'),(2,'vip'),(3,'generic'))
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_token  = models.CharField(max_length=255,null=True)
    user_type = models.SmallIntegerField(choices=choices)


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    publish = models.ForeignKey(to='Publish',on_delete=models.SET_NULL,null=True)


class Publish(models.Model):
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
