from django.urls import path
from export_app.views import staff_member_required

from . import views

urlpatterns = [
    path('', staff_member_required(views.projects_list), name='projects_list'),
    path('update_projects/', staff_member_required(views.update_projects), name='update_projects'),
    path('<int:project_id>/', staff_member_required(views.project), name='project'),
    path('update_project/', staff_member_required(views.update_project), name='update_project'),
    path('get_status_project/<task_id>/', staff_member_required(views.get_status_project), name='get_status_project'),
    path('<int:project_id>/page/<int:page_id>/', staff_member_required(views.page), name='page'),
    path('<int:project_id>/page/<int:page_id>/update_page/', staff_member_required(views.update_page), name='update_page'),
    path('sentry-debug/', staff_member_required(views.trigger_error), name="sentry_debug"),
]
