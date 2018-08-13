from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('update_projects/', views.update_projects, name='update_projects'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:project_id>/update_project/', views.update_project, name='update_project'),
]
