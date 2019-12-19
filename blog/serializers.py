# -*- encoding: utf-8 -*-
"""
@File:      serializers.py.py
@Time:      2019/11/24 11:53 AM
@Author:    Colin
@Email:     bsply@126.com
@Software:  PyCharm
"""
from django.db.models import Count
from .models import Category, Tag, Post, Course
# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from rest_framework.response import Response


class PostNormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'







class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'count')

    def get_count(self, obj):
        categories = Category.objects.annotate(count=Count('post')).filter(count__gt=0, name=obj.name)
        if categories:
            return categories[0].count
        else:
            return 0


class TagSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(default=0)

    class Meta:
        model = Tag
        fields = '__all__'

    def get_count(self, obj):
        tags = Tag.objects.annotate(counts=Count('post')).filter(counts__gt=0, name=obj.name)
        if tags:
            return tags[0].counts
        else:
            return 0


class PostSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    tag = TagSerializer(many=True)
    # course = serializers.CharField(source='course.name')
    course = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Post
        fields = ('id', 'title', 'abstract', 'content', 'category', 'tag', 'view', 'course', 'createTime')

    def get_course(self, obj):
        post = Post.objects.get(pk=obj.id)
        if post.course:
            return {'name': post.course.name, 'id':post.course.id}
        else:
            return None


class CourseSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'type', 'posts', 'description')

    def get_posts(self, obj):
        course = Course.objects.filter(name=obj.name).first()
        sum_view = 0
        if course:
            posts = course.post_set.all()
            posts_json = serialize("json", list(posts), fields=('title', 'createTime', 'view'))
            posts_json = json.loads(posts_json)
            for post in posts_json:
                sum_view += post['fields']['view']
        return {'sum_view': sum_view, 'posts': posts_json}
        # return posts_json

