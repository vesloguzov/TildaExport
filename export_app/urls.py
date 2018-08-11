from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('/update_projects', views.update_projects, name='update_projects'),
]
