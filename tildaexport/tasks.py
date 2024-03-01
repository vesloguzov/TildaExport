from celery import shared_task, current_task
from django.conf import settings
from datetime import datetime
import pytz as tz
import logging
import time
from decimal import *
import requests
import os
import json

from export_app.models import TildaRequest, RelationTaskProject, Project
from django_celery_results.models import TaskResult
from django_celery_results.managers import TaskResultManager

my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


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
    # tr.getpageslistcount(project_id)
    objects_count = 0
    # self.update_state(
    #     state="PROGRESS",
    #     meta={
    #         "project_id": project_id,
    #         "total": 100,
    #         "page_count": percent,
    #     },
    # )
    # tr.getprojectexport(project_id)
    # self.update_state(
    #     state="PROGRESS",
    #     meta={
    #         "project_id": project_id,
    #         "total": 100,
    #         "page_count": 0,
    #     },
    # )

    # if tr.request_count < tr.requests_limit:
    #     request = requests.get(
    #         "{}getpageslist/?publickey={}&secretkey={}&projectid={}".format(
    #             tr.base_url, tr.publickey, tr.secretkey, project_id
    #         )
    #     )
    #     if tr.is_available():
    #         tr.increment()
    #         response = request.json()
    #         project = Project.objects.get(pk=project_id)
    #         if response["status"] == "FOUND" and response["result"] is not None:
    #             tr.pages.clear()
    #             for page in response["result"]:
    #                 page_object = project.ProjectPages.get_or_create(id=page["id"])[0]
    #                 page_object.projectid = page["projectid"]
    #                 page_object.title = page["title"]
    #                 page_object.descr = page["descr"]
    #                 page_object.img = page["img"]
    #                 page_object.featureimg = page["featureimg"]
    #                 page_object.alias = page["alias"]
    #                 page_object.date = page["date"]
    #                 page_object.sort = page["sort"]
    #                 page_object.published = page["published"]
    #                 page_object.filename = page["filename"]
    #                 page_object.save()
    #                 tr.pages.add(page_object)
    #                 objects_count += 1
    # percent = (
    #     Decimal(objects_count) / Decimal(project.total_objects)
    # ) * Decimal(100)
    # percent = float(round(percent, 2))
    #                 # for percent in range(99):
    #                 self.update_state(
    #                     state="PROGRESS",
    #                     meta={
    #                         "project_id": project_id,
    #                         "total": 100,
    #                         "page_count": percent,
    #                     },
    #                 )
    #                 time.sleep(0.05)
    #             tr.save()
    #         return True
    #     else:
    #         return False
    # up = UpdateProject(task=self, project_id=project_id)
    # up.run()
    logging.warning(rel.project_id)
    tr.getprojectexport(rel.project_id)
    tr.getpageslist(rel.project_id)
    return json.dumps(
        {
            "project_id": project_id,
            "total": 100,
            "page_count": 100,
        }
    )
    # get_project = tr.getprojectexport(project_id)
    # if (get_project):
    #     tr.getpageslist(project_id)


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
