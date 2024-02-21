from celery import shared_task
from export_app.models import TildaRequest

@shared_task
def update_project_task(project_id):
    tr = TildaRequest.objects.filter(projects__pk=project_id).latest("id")
    tr.getprojectexport(project_id)
    return tr.getpageslist(project_id)