from celery import shared_task, current_task
from export_app.models import TildaRequest
import logging
import time

@shared_task(bind=True)
def update_project_task(self, project_id, page_count):
    logging.warning('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    logging.warning(project_id)
    logging.warning(self)
    tr = TildaRequest.objects.filter(projects__pk=project_id).latest("id")
    logging.warning(tr)
    current_task.update_state(state='PROGRESS', meta={'total': page_count,'project_id': project_id})
    time.sleep(5)

    # get_project = tr.getprojectexport(project_id)
    # if (get_project):
    #     tr.getpageslist(project_id)