# -*- encoding: utf-8 -*-
"""
@File:      viewsets.py.py
@Time:      2019/11/24 11:56 AM
@Author:    Colin
@Email:     bsply@126.com
@Software:  PyCharm
"""

from blog.models import Category, Tag, Post, Course
from blog.pagination import StandardResultsSetPagination

from blog.serializers import CategorySerializer, TagSerializer, PostSerializer, PostNormalSerializer
from blog.serializers import CourseSerializer

from django.db.models import Count
from django.core.serializers import serialize

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

import json


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True)
    def posts(self, request, *args, **kwargs):
        posts = Category.objects.get(pk=self.kwargs['pk'])
        posts_set = posts.post_set.all()
        posts_json = serialize("json", list(posts_set), fields=('title', 'createTime'))
        posts_json = json.loads(posts_json)
        result = {'code': 200, 'msg': 'success', 'posts': posts_json, 'name': posts.name}
        return Response(result)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=True)
    def posts(self, request, *args, **kwargs):
        posts = Tag.objects.get(pk=self.kwargs['pk'])
        posts_set = posts.post_set.all()
        posts_json = serialize("json", list(posts_set), fields=('title', 'createTime'))
        posts_json = json.loads(posts_json)
        result = {'code': 200, 'msg': 'success', 'posts': posts_json, 'name': posts.name}
        return Response(result)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increase_view()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all().order_by('-updateTime')
        # 实例化分页对象，获取数据库中的分页数据
        paginator = StandardResultsSetPagination()
        page_post_list = paginator.paginate_queryset(queryset, self.request, view=self)
        # 序列化对象
        serializer = PostSerializer(page_post_list, many=True)
        # 生成分页和数据
        response = paginator.get_paginated_response(serializer.data)
        return response

    @action(detail=False)
    def archive(self, request, *args, **kwargs):
        # return Response('post archive')
        post_year = Post.objects.values('createTime__year').annotate(count=Count('createTime__year')).order_by(
            '-createTime__year')
        res_posts = []
        for year in post_year:
            posts = Post.objects.filter(createTime__year=year['createTime__year']).order_by('-createTime')
            posts_json = serialize("json", list(posts), fields=('title', 'createTime'))
            posts_json = json.loads(posts_json)
            result = {'year': year['createTime__year'], 'count': year['count'], 'posts': posts_json}
            res_posts.append(result)
        return Response(res_posts)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        course_type_counts = Course.objects.values('type').annotate(count=Count('type'))
        result = []
        for course_type_count in course_type_counts:
            courses = Course.objects.filter(type=course_type_count['type'])
            courses_json = serialize('json', list(courses))
            courses_json = json.loads(courses_json)
            sum_view = 0
            for course in courses_json:
                posts = Post.objects.filter(course__name=course['fields']['name'])
                for post in posts:
                    sum_view += post.view
                course['fields']['sum_view'] = sum_view

            result_item = {'type': course_type_count['type'], 'count': course_type_count['count'], 'courses': courses_json}
            result.append(result_item)
        return Response(result)