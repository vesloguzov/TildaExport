# from django.http import Http404, JsonResponse
import json
from django.shortcuts import render, redirect
from django.core import serializers
from export_app.models import Project, TildaRequest

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from django.conf import settings


def staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url=settings.LOGIN_URL):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


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
    project = Project.objects.get(pk=project_id)
    page = project.ProjectPages.all().get(pk=page_id)
    context = dict()
    context["page"] = page
    context["project"] = project
    # print(context)
    return render(request, "page.html", context)


def update_page(request, project_id, page_id):
    tr = TildaRequest.objects.latest("id")
    tr.getpagefullexport(project_id, page_id)
    return redirect("/projects/{}/page/{}/".format(project_id, page_id))
