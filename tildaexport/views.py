# from django.http import Http404, JsonResponse
from django.shortcuts import render
import datetime
import json
from .models import Project


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
    return render(request, "base.html", context)
