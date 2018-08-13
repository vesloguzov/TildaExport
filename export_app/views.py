# from django.http import Http404, JsonResponse
import json
from django.shortcuts import render, redirect
from django.core import serializers
from export_app.models import Project, TildaRequest


def projects_list(request):
    context = dict()
    context["projects"] = []
    for project in Project.objects.all():
        context["projects"].append({
            "id": project.id,
            "title": project.title,
            "descr": project.descr
        }
        )
    return render(request, "projects.html", context)


def update_projects(request):
    tr = TildaRequest.objects.latest("id")
    tr.getprojectslist()
    print("TildaRequest.objects.latest()", TildaRequest.objects.latest("id"))
    return redirect("/projects/")


def project(request, project_id):
    project = Project.objects.get(pk=project_id)
    context = dict()
    context["project"] = project
    context["pages"] = []
    for page in project.ProjectPages.all():
        context["pages"].append(page)
    return render(request, "project.html", context)


def update_project(request, project_id):
    tr = TildaRequest.objects.latest("id")
    tr.getprojectexport(project_id)
    tr.getpageslist(project_id)
    return redirect("/projects/{}/".format(project_id))


def page(request, project_id, page_id):
    page = Project.objects.get(pk=project_id).ProjectPages.all().get(pk=page_id)
    context = dict()
    context["page"] = page
    return render(request, "page.html", context)


def update_page(request, project_id, page_id):
    tr = TildaRequest.objects.latest("id")
    tr.getpagefullexport(project_id, page_id)
    return redirect("/projects/{}/page/{}/".format(project_id, page_id))
