from django.db import models
from django.utils import timezone


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        # ordering = [""]
        # verbose_name = ""
        # verbose_name_plural = verbose_name
        db_table = 'app01_tag'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'app01_category'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    tag = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'app01_post'

    def __str__(self):
        return self.title

