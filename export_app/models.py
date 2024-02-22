import os
from datetime import datetime

import pytz as tz
import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
import logging


# log = logging.getLogger(__name__)
my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def is_binary(obj):
    try:
        str(obj)
        return True
    except TypeError:
        return False


def get_site_addr():
    site = Site.objects.get_current()
    if settings.USE_SSL:
        site = "https://{}".format(site.domain)
    else:
        site = "http://{}".format(site.domain)
    return site


class TildaRequest(models.Model):
    name = models.CharField("Имя", max_length=255, null=True, blank=True)
    request_count = models.IntegerField("Количество запросов за час", default=0)
    publickey = models.CharField(
        null=False, blank=False, max_length=20, default="5iusv518bgyj2ox69cpi"
    )
    secretkey = models.CharField(
        null=False, blank=False, max_length=20, default="wyf7n1weosiuacn6hoft"
    )
    base_url = "http://api.tildacdn.info/v1/"
    requests_limit = 140
    created_at = models.DateTimeField(auto_now_add=True)

    projects = models.ManyToManyField("Project", blank=True)
    pages = models.ManyToManyField("Page", blank=True)
    # count = models.IntegerField("Количество запросов за час", null=True, blank=True)

    def is_available(self):
        now = datetime.now(tz.timezone(settings.TIME_ZONE))
        timedelta = now - self.created_at

        if timedelta.total_seconds() > 3600:
            self.request_count = 0
            self.created_at = now
            self.save()
            return True
        elif self.request_count < self.requests_limit:
            return True
        else:
            return False

    def increment(self):
        self.request_count = self.request_count + 1
        self.save()

    def getprojectslist(self):
        print("_____________")
        print(
            "{}getprojectslist/?publickey={}&secretkey={}".format(
                self.base_url, self.publickey, self.secretkey
            )
        )
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getprojectslist/?publickey={}&secretkey={}".format(
                    self.base_url, self.publickey, self.secretkey
                )
            )
            print(self.name)
            if self.is_available():
                self.increment()
                response = request.json()
                if response["status"] == "FOUND":
                    self.projects.clear()
                    for project in response["result"]:
                        project_object = Project.objects.get_or_create(
                            id=project["id"]
                        )[0]
                        project_object.title = project["title"]
                        project_object.descr = project["descr"]
                        project_object.save()
                        self.projects.add(project_object)
                    self.save()
                    return True
            else:
                return False

    def getprojectexport(self, project_id):
        print("TEST")
        print(
            "{}getprojectexport/?publickey={}&secretkey={}&projectid={}".format(
                self.base_url, self.publickey, self.secretkey, project_id
            )
        )
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getprojectexport/?publickey={}&secretkey={}&projectid={}".format(
                    self.base_url, self.publickey, self.secretkey, project_id
                )
            )
            if self.is_available():
                self.increment()
                response = request.json()
                project = Project.objects.get(pk=project_id)
                if response["status"] == "FOUND":
                    project.id = response["result"]["id"]
                    project.title = response["result"]["title"]
                    project.descr = response["result"]["descr"]
                    project.customdomain = response["result"]["customdomain"]
                    project.export_csspath = response["result"]["export_csspath"]
                    project.export_jspath = response["result"]["export_jspath"]
                    project.export_imgpath = response["result"]["export_imgpath"]
                    project.indexpageid = response["result"]["indexpageid"]
                    project.last_updated = datetime.now()
                    project.save()
                    # if ("js" or "css" or "images") in response["result"].keys():

                    if "js" in response["result"].keys():
                        project.save_static_files(response["result"]["js"])
                    if "css" in response["result"].keys():
                        project.save_static_files(response["result"]["css"])
                    if "images" in response["result"].keys():
                        project.save_static_files(response["result"]["images"])
                    return True
            else:
                return False

    def getpageslist(self, project_id):
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getpageslist/?publickey={}&secretkey={}&projectid={}".format(
                    self.base_url, self.publickey, self.secretkey, project_id
                )
            )
            if self.is_available():
                self.increment()
                response = request.json()
                project = Project.objects.get(pk=project_id)
                if response["status"] == "FOUND" and response["result"] is not None:
                    self.pages.clear()
                    for page in response["result"]:
                        page_object = project.ProjectPages.get_or_create(id=page["id"])[
                            0
                        ]
                        page_object.projectid = page["projectid"]
                        page_object.title = page["title"]
                        page_object.descr = page["descr"]
                        page_object.img = page["img"]
                        page_object.featureimg = page["featureimg"]
                        page_object.alias = page["alias"]
                        page_object.date = page["date"]
                        page_object.sort = page["sort"]
                        page_object.published = page["published"]
                        page_object.filename = page["filename"]
                        page_object.save()
                        self.pages.add(page_object)
                    self.save()
                return True
            else:
                return False

    def getpageslistcount(self, project_id):
        count = 0
        if self.request_count < self.requests_limit:
            request_getpageslist = requests.get(
                "{}getpageslist/?publickey={}&secretkey={}&projectid={}".format(
                    self.base_url, self.publickey, self.secretkey, project_id
                )
            )
            request_getprojectexport = requests.get(
                "{}getprojectexport/?publickey={}&secretkey={}&projectid={}".format(
                    self.base_url, self.publickey, self.secretkey, project_id
                )
            )
            if self.is_available():
                self.increment()
                response_getpageslist = request_getpageslist.json()
                response_getprojectexport = request_getprojectexport.json()
                if (
                    response_getpageslist["status"] == "FOUND"
                    and response_getpageslist["result"] is not None
                ) and (
                    response_getprojectexport["status"] == "FOUND"
                    and response_getprojectexport["result"] is not None
                ):
                    if "js" in response_getprojectexport["result"].keys():
                        count += len(response_getprojectexport["result"]["js"])
                    if "css" in response_getprojectexport["result"].keys():
                        count += len(response_getprojectexport["result"]["css"])
                    if "images" in response_getprojectexport["result"].keys():
                        count += len(response_getprojectexport["result"]["images"])
                    count += len(response_getpageslist["result"])
                    project = Project.objects.get(pk=project_id)
                    project.children_objects_count = count
                    project.save()
                    return count
            else:
                return 0

    def getpagefullexport(self, page_id):
        # logging.warning("TEST")
        if self.request_count < self.requests_limit:
            # logging.info("TETE")
            request = requests.get(
                "{}getpagefullexport/?publickey={}&secretkey={}&pageid={}".format(
                    self.base_url, self.publickey, self.secretkey, page_id
                )
            )
            if self.is_available():
                self.increment()
                response = request.json()
                if response["status"] == "FOUND":
                    page = response["result"]
                    page_object = Page.objects.get(pk=page_id)
                    page_object.projectid = page["projectid"]
                    page_object.title = page["title"]
                    page_object.descr = page["descr"]
                    page_object.img = page["img"]
                    page_object.featureimg = page["featureimg"]
                    page_object.alias = page["alias"]
                    page_object.date = page["date"]
                    page_object.sort = page["sort"]
                    page_object.published = page["published"]
                    page_object.filename = page["filename"]
                    if page["html"] is not None:
                        # print(page["html"])
                        page_object.html = page["html"].replace(
                            "</head>",
                            '<script type="text/javascript" src="{}/static/js/iframeResizer.contentWindow.min.js"></script></head>'.format(
                                get_site_addr()
                            ),
                        )
                        page_object.html = page_object.html.replace("height:100vh;", "")
                    else:
                        page_object.html = ""
                    page_object.last_updated = datetime.now()
                    page_object.save()
                    if "js" in response["result"].keys():
                        page_object.save_static_files(response["result"]["js"])
                    if "css" in response["result"].keys():
                        page_object.save_static_files(response["result"]["css"])
                    if "images" in response["result"].keys():
                        page_object.save_page_images(response["result"]["images"])
                    page_object.save_html_file()
                    return True
            else:
                return False


class Project(models.Model):
    id = models.CharField(
        "Идентификатор", max_length=255, null=False, blank=False, primary_key=True
    )
    title = models.CharField("Название", max_length=255, null=False, blank=False)
    descr = models.TextField("Описание", null=True, blank=True)
    customdomain = models.CharField("Домен", max_length=255, null=True, blank=True)
    export_csspath = models.CharField(
        "Путь экспорта", max_length=255, null=True, blank=True
    )
    export_jspath = models.CharField(
        "Путь экспорта", max_length=255, null=True, blank=True
    )
    export_imgpath = models.CharField(
        "Путь экспорта", max_length=255, null=True, blank=True
    )
    indexpageid = models.CharField("indexpageid", max_length=255, null=True, blank=True)
    static_files = models.ManyToManyField("StaticFile", blank=True)
    ProjectPages = models.ManyToManyField("Page", blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    children_objects_count = models.IntegerField(null=True, blank=True)

    def save_static_files(self, files):
        # my_headers = {}
        # my_headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        # TODO: tr.getpageslistcount(self.id); count -- ; and pass to task.py and create progress bar.
        for file in files:
            path = os.path.join(settings.MEDIA_ROOT, "projects", self.id)
            newfile = os.path.join(settings.MEDIA_ROOT, "projects", self.id, file["to"])
            if not os.path.isdir(path):
                os.mkdir(path)
            response = requests.get(file["from"], headers=my_headers)
            # headers=my_headers
            with open(newfile, "w") as out_file:
                out_file.write(response.text)


class Page(models.Model):
    id = models.CharField(
        "Идентификатор", max_length=255, null=False, blank=False, primary_key=True
    )
    projectid = models.CharField("Проект", max_length=255, null=False, blank=False)
    title = models.CharField("Название", max_length=255, null=False, blank=False)
    descr = models.TextField("Описание", max_length=16000, null=True, blank=True)
    img = models.CharField("Картинка", max_length=255, null=True, blank=True)
    featureimg = models.CharField("featureimg", max_length=255, null=True, blank=True)
    alias = models.CharField("alias", max_length=255, null=True, blank=True)
    date = models.CharField("Дата создания", max_length=255, null=True, blank=True)
    sort = models.CharField(
        "Номер очередности в списке страниц", max_length=255, null=True, blank=True
    )
    published = models.CharField(
        "Адрес страницы", max_length=255, null=True, blank=True
    )
    filename = models.CharField("Имя файла", max_length=255, null=True, blank=True)
    static_files = models.ManyToManyField("StaticFile", blank=True)
    html = models.TextField("HTML", default="")
    page_path = models.CharField(
        "Адрес страницы на сервере", max_length=255, null=True, blank=True
    )
    iframe = models.TextField("IFrame code", default="")
    last_updated = models.DateTimeField(null=True, blank=True)

    def save_iframe_code(self):
        # print(self.filename.split('.')[0])

        self.iframe = '<iframe src="{}" webkitallowfullscreen="" mozallowfullscreen="" allowfullscreen=""  id="{}" width="100%" onload=\'var tag = "script";var scriptTag = document.createElement(tag);var firstScriptTag = document.getElementsByTagName(tag)[0]; scriptTag.src = "{}";firstScriptTag.parentNode.insertBefore(scriptTag, firstScriptTag);{}\' frameborder="0" scrolling="no"></iframe><style>.window-wrap {{height: auto !important;}}</style>'.format(
            get_site_addr() + self.page_path,
            self.filename.split(".")[0],
            get_site_addr() + "/static/js/iframeResizer.min.js",
            'scriptTag.onload = function(){{iFrameResize({{log: true, checkOrigin: false, heightCalculationMethod : "lowestElement"}}, "#{}")}}'.format(
                self.filename.split(".")[0]
            ),
        )
        pass

    def save_html_file(self):
        path = os.path.join(settings.MEDIA_ROOT, "projects", self.projectid)
        newfile = os.path.join(
            settings.MEDIA_ROOT, "projects", self.projectid, self.filename
        )
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(newfile, "w") as out_file:
            out_file.write(self.html)
        self.page_path = os.path.join(
            settings.MEDIA_URL, "projects", self.projectid, self.filename
        )
        self.save()
        self.save_iframe_code()
        self.save()

    def save_page_images(self, files):
        # my_headers = {}
        # my_headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        for file in files:
            path = os.path.join(settings.MEDIA_ROOT, "projects", self.projectid)
            newfile = os.path.join(
                settings.MEDIA_ROOT, "projects", self.projectid, file["to"]
            )
            if not os.path.isdir(path):
                os.mkdir(path)
            response = requests.get(file["from"], stream=True, headers=my_headers)
            if is_binary(response):
                with open(newfile, "wb") as out_file:
                    for chunk in response:
                        out_file.write(chunk)
            else:
                with open(newfile, "w") as out_file:
                    out_file.write(response.text)

    def save_static_files(self, files):
        #        my_headers = {}
        # 	my_headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        for file in files:
            path = os.path.join(settings.MEDIA_ROOT, "projects", self.id)
            newfile = os.path.join(settings.MEDIA_ROOT, "projects", self.id, file["to"])
            if not os.path.isdir(path):
                os.mkdir(path)
            response = requests.get(file["from"], headers=my_headers)
            # logging.warning(response)
            with open(newfile, "w") as out_file:
                out_file.write(response.text)


class StaticFile(models.Model):
    filename = models.CharField("Имя файла", max_length=255, null=False, blank=False)
    type = (("image", "Картинка"), ("js", "JavaScript-файл"), ("css", "CSS-файл"))
    path = models.CharField("Путь у нас", max_length=255, null=False, blank=False)
    path_tilda = models.CharField("Путь у них", max_length=255, null=False, blank=False)
