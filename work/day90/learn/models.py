from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


# 使用默认django 原生的auth表
class User(AbstractUser):
    mobile = models.CharField(max_length=64)


class Userinfo(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=255)


class BaseClass(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Book(BaseClass):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    publish = models.ForeignKey(to='Publish',on_delete=models.SET_NULL,null=True
                                ,db_constraint=False)
    author = models.ManyToManyField(to='Author',db_constraint=False,)

    @property
    def publishes(self):
        return self.publish.name

    @property
    def authors(self):
        return  [{'id':user.pk,'name':user.name,'mobile':user.mobile} for user in self.author.all()]



class Publish(BaseClass):
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)


class Author(BaseClass):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
