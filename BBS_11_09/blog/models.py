from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    head = models.FileField(upload_to='head/', default='head/default.png')
    phone = models.CharField(max_length=25)
    blog = models.OneToOneField(to='blog', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'


class Blog(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客'

        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField(max_length=255)
    blog = models.ForeignKey(to='blog', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '分类'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    blog = models.ForeignKey(to='blog', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '标签'


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    down_num = models.IntegerField(default=0)
    up_num = models.IntegerField(default=0)
    commit_num = models.IntegerField(default=0)
    content = models.TextField()
    blog = models.ForeignKey(to='blog', on_delete=models.CASCADE)
    tag = models.ManyToManyField(to='Tag')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章详情'


class Comment(models.Model):
    user = models.CharField(max_length=255)
    article = models.ForeignKey(on_delete=models.CASCADE, to='Article')
    content = models.CharField(max_length=255)
    Comment_id = models.ForeignKey(to='self',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = '评论'


class UpAndDown(models.Model):
    user = models.CharField(max_length=255)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    is_up = models.BooleanField()
    id_down = models.BooleanField(null=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = '点赞'
