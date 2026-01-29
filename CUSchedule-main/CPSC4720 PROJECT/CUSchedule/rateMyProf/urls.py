from django.urls import path
from . import views

#list of url patterns that the user can route to
urlpatterns = [
    path('', views.home_view, name="home"),
    path('rmpSearch/', views.prof_search, name="search"),
    path('rmpSearch/', views.prof_search_result, name="search_result"),
    path('courseInfo/', views.course_search, name="course_search"),
    path('courseInfoSearchResult/', views.course_search_result, name="course_search_result"),
    path('schedule-builder/', views.schedule_builder, name="schedule_builder"),
]
