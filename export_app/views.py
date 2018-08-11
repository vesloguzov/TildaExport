# from django.http import Http404, JsonResponse
from django.shortcuts import render
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
    TildaRequest.objects.latest(field_name=None).getprojectslist()
    projects_list(request)
