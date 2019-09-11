# encoding: utf-8

from django.urls import path, include
from rest_framework import routers
from app01 import views 

router = routers.DefaultRouter()
router.register('post', views.PostViewSet)
router.register('tag', views.TagViewSet)
router.register('category', views.CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]