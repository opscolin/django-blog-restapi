from django.db import models
from uuslug import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Course(models.Model):
    choice_type = (
        (1, 'django'),
        (2, 'djangovue'),
        (3, 'devops'),
    )
    name = models.CharField(max_length=120)
    type = models.SmallIntegerField(choices=choice_type, default=3)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=120)
    abstract = models.CharField(max_length=200, null=True, default='', blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    createTime = models.DateField()
    updateTime = models.DateField()
    url_slug = models.SlugField(editable=False)

    # view count
    view = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-createTime']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def increase_view(self):
        self.view += 1
        self.save(update_fields=['view'])




