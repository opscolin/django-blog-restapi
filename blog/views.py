from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Post, Category, Tag, Course
from rest_framework import serializers
import json
from blog.serializers import PostSerializer
from django.core.serializers import serialize

from django.db.models import Count


# Create your views here.
class TagPosts(APIView):
    """
    get post list belong to some tag
    """
    def get(self, request, tag):
        posts = Tag.objects.filter(name=tag).first()
        posts_set = posts.post_set.all()
        posts_json = serialize("json", list(posts_set), fields=('title', 'createTime'))
        posts_json = json.loads(posts_json)
        result = {'code': 200, 'msg': 'success', 'posts': posts_json}
        return Response(result)


class CategoryPosts(APIView):
    """
    get post list belong to some category
    """
    def get(self, request, category):
        posts = Category.objects.filter(name=category).first()
        posts_set = posts.post_set.all()
        print(type(posts_set))
        posts_json = serialize("json", list(posts_set), fields=('title', 'createTime'))
        posts_json = json.loads(posts_json)
        result = {'code': 200, 'msg': 'success', 'posts': posts_json}
        return Response(result)


class PostsArchive(APIView):
    """
    get post list group by year to archive
    """
    def get(self, request):
        post_year = Post.objects.values('createTime__year').annotate(count=Count('createTime__year')).order_by('-createTime__year')
        res_posts = []
        for year in post_year:
            posts = Post.objects.filter(createTime__year=year['createTime__year']).order_by('-createTime')
            posts_json = serialize("json", list(posts), fields=('title', 'createTime'))
            posts_json = json.loads(posts_json)
            result = {'year': year['createTime__year'], 'count': year['count'], 'posts': posts_json}
            res_posts.append(result)
        return Response(res_posts)
