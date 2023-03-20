from django.urls import path
from . import views
from .views import (post_like)
from my_site import views

app_name = 'my_site'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('like/', views.post_like, name='like'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('search/', views.search, name='search'),
    path('contact/', views.ContactView.as_view(), name='contact'),

]

