from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
import logging

from export_app.models import Project, TildaRequest


def staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url=settings.LOGIN_URL):
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
    for _project in Project.objects.all():
        context["projects"].append({
            "id": _project.id,
            "title": _project.title,
            "descr": _project.descr
        })
    return render(request, "projects.html", context)


def update_projects(request):
    # tr = TildaRequest.objects.latest("id")
    for tilda_request in TildaRequest.objects.all():
        request_result = tilda_request.getprojectslist()
        print("RESULT:", request_result)
        if not request_result:
            return render(request, "counter_except.html")
    # else:
    #
    return redirect("/projects/")


def project(request, project_id):
    _project = Project.objects.get(pk=project_id)
    context = dict()
    context["project"] = _project
    context["pages"] = []
    for _page in _project.ProjectPages.all():
        context["pages"].append(_page)
    return render(request, "project.html", context)


def update_project(request, project_id):
    tr = TildaRequest.objects.filter(projects__pk=project_id).latest("id")
    if tr.getprojectexport(project_id) and tr.getpageslist(project_id):
        return redirect("/projects/{}/".format(project_id))
    else:
        return render(request, "counter_except.html")


def page(request, project_id, page_id):
    _project = Project.objects.get(pk=project_id)
    _page = _project.ProjectPages.all().get(pk=page_id)
    context = dict()
    context["page"] = _page
    context["project"] = _project
    #logging.warning("TEST")
    #logging.info("TEST@")
    return render(request, "page.html", context)


def update_page(request, project_id, page_id):
    tr = TildaRequest.objects.filter(projects__pk=project_id).latest("id")
    if tr.getpagefullexport(page_id):
        return redirect("/projects/{}/page/{}/".format(project_id, page_id))
    else:
        return render(request, "counter_except.html")


def trigger_error(request):
    division_by_zero = 1 / 0
