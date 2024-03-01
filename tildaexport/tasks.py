from celery import shared_task
from django.conf import settings
from datetime import datetime
import pytz as tz
import logging
import time
from decimal import *
import json

from export_app.models import TildaRequest, RelationTaskProject, Project


@shared_task(bind=True)
def update_project_task(self, project_id):
    logging.warning(project_id)
    logging.warning(self)
    tr = TildaRequest.objects.filter(projects__pk=project_id).latest("id")
    rel, created = RelationTaskProject.objects.get_or_create(
        task_id=self.request.id,
        project_id=project_id,
        created_at=datetime.now(tz.timezone(settings.TIME_ZONE)),
    )
    project = Project.objects.get(id=project_id)
    if project.objects_count > 0:
        project.objects_count = 0
        project.save()
    tr.getpageslistcount(project_id)
    tr.getprojectexport(rel.project_id)
    tr.getpageslist(rel.project_id)
    return json.dumps(
        {
            "project_id": project_id,
            "total": 100,
            "page_count": 100,
        }
    )


class UpdateProject(object):
    def __init__(self, task, project_id):
        self.task = task
        self.project_id = project_id

    def run(self):
        for percent in range(100):
            self.task.update_state(
                state="PROGRESS",
                meta={
                    "project_id": self.project_id,
                    "total": 100,
                    "page_count": percent,
                },
            )
            time.sleep(0.05)
