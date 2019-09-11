# encoding: utf-8

from django.shortcuts import render
from rest_framework import viewsets

from app01.models import Post, Tag, Category
from app01.serializers import PostSerializer, TagSerializer, CategorySerializer

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-create_time')
    serializer_class = PostSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer