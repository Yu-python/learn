from django.db import models

# Create your models here.


class Book(models.Model):
    id = models.AutoField(primary_key=True,help_text='id')
    title = models.CharField(max_length=255,help_text='标题')
    price = models.DecimalField(max_digits=5,decimal_places=2,help_text='价格')
    publish = models.CharField(max_length=255,help_text='出版社')
