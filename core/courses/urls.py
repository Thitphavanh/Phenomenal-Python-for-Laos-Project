from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course listing and detail
    path('', views.course_list, name='course_list'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('pricing/', views.pricing, name='pricing'),
    path('instructor/<str:username>/', views.instructor_profile, name='instructor_profile'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),

    # Enrollment
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),

    # Lessons
    path('<slug:course_slug>/lesson/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:course_slug>/lesson/<slug:lesson_slug>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
]
