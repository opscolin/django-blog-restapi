from django.contrib import admin
from .models import Tag, Category, Post, Course
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Course)
