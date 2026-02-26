from django.urls import path
from . import views

app_name = 'docs'

urlpatterns = [
    path('', views.doc_list, name='doc_list'),
    path('category/<slug:slug>/', views.category_docs, name='category_docs'),
    path('<slug:slug>/', views.doc_detail, name='doc_detail'),
]
