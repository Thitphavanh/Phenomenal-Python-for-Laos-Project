from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='index'),
    path('create/', views.CreateTopicView.as_view(), name='create_topic'),
    path('topic/<slug:slug>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<slug:slug>/reply/', views.create_reply, name='create_reply'),
]
