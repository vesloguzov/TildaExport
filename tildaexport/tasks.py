from celery import shared_task, current_task
from django.conf import settings
from datetime import datetime
import pytz as tz
import logging
import time

from export_app.models import TildaRequest, RelationTaskProject
from django_celery_results.models import TaskResult
from django_celery_results.managers import TaskResultManager


@shared_task(bind=True)
def update_project_task(self, project_id, total):
    logging.warning(project_id)
    logging.warning(self)
    tr = TildaRequest.objects.filter(projects__pk=project_id).latest("id")
    RelationTaskProject.objects.get_or_create(
        task_id=self.request.id,
        project_id=project_id,
        created_at=datetime.now(tz.timezone(settings.TIME_ZONE)),
    )
    for page_count in range(total + 1):
        self.update_state(
            state="PROGRESS",
            meta={
                "project_id": project_id,
                "total": total,
                "page_count": page_count,
            },
        )
        time.sleep(0.1)
    return {
        "project_id": project_id,
        "total": total,
        "page_count": page_count,
    }

    # get_project = tr.getprojectexport(project_id)
    # if (get_project):
    #     tr.getpageslist(project_id)
