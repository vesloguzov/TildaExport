# from time import gmtime
from django.db import models
import requests
from django.conf import settings
import json
import shutil
import os


class TildaRequest(models.Model):
    name = models.CharField("Имя", max_length=255, null=True, blank=True)
    request_count = models.IntegerField("Количество запросов за час", default=0)
    publickey = "ptjpckc4gc0feyrbgj0w"
    secretkey = "787nil2glnhbg00skcx1"
    base_url = "http://api.tildacdn.info/v1/"
    requests_limit = 120

    def increment(self):
        self.request_count = self.request_count + 1
        self.save()

    def getprojectslist(self):
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getprojectslist/?publickey={}&secretkey={}".format(self.base_url, self.publickey, self.secretkey))
            self.increment()
            response = request.json()
            if response["status"] == "FOUND":
                for project in response["result"]:
                    project_object = Project.objects.get_or_create(id=project["id"])[0]
                    project_object.title = project["title"]
                    project_object.descr = project["descr"]
                    project_object.save()

    def getprojectexport(self, project_id):
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getprojectexport/?publickey={}&secretkey={}&projectid={}".format(self.base_url, self.publickey,
                                                                                    self.secretkey, project_id))
            self.increment()
            response = request.json()
            project = Project.objects.get(pk=project_id)
            if response["status"] == "FOUND":
                print("id", response["result"]["id"])
                project.id = response["result"]["id"]
                project.title = response["result"]["title"]
                project.descr = response["result"]["descr"]
                project.customdomain = response["result"]["customdomain"]
                project.export_csspath = response["result"]["export_csspath"]
                project.export_jspath = response["result"]["export_jspath"]
                project.export_imgpath = response["result"]["export_imgpath"]
                project.indexpageid = response["result"]["indexpageid"]
                project.save()
                # project.save_static_files('js', response["result"]["js"])
                project.save_static_files('css', response["result"]["css"])
                # project.save_static_files('image', response["result"]["images"])

                # project.
                # project.

    def getpageslist(self, project_id):
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getpageslist/?publickey={}&secretkey={}&projectid={}".format(self.base_url, self.publickey,
                                                                                self.secretkey, project_id))
            self.increment()
            response = request.json()
            project = Project.objects.get(pk=project_id)
            if response["status"] == "FOUND" and response["result"] != None:
                for page in response["result"]:
                    page_object = project.ProjectPages.get_or_create(id=page["id"])[0]
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


class Project(models.Model):
    id = models.CharField("Идентификатор", max_length=255, null=False, blank=False, primary_key=True)
    title = models.CharField("Название", max_length=255, null=False, blank=False)
    descr = models.CharField("Описание", max_length=255, null=True, blank=True)
    customdomain = models.CharField("Домен", max_length=255, null=True, blank=True)
    export_csspath = models.CharField("Путь экспорта", max_length=255, null=True, blank=True)
    export_jspath = models.CharField("Путь экспорта", max_length=255, null=True, blank=True)
    export_imgpath = models.CharField("Путь экспорта", max_length=255, null=True, blank=True)
    indexpageid = models.CharField("indexpageid", max_length=255, null=True, blank=True)
    # favicon = models.CharField("Картинка", max_length=255, null=True, blank=True)
    # page404id = models.CharField("page404id", max_length=255, null=True, blank=True)
    static_files = models.ManyToManyField('StaticFile', blank=True)
    # js = models.ManyToManyField('StaticFile')
    # css = models.ManyToManyField('StaticFile')
    ProjectPages = models.ManyToManyField('Page', blank=True)

    def save_static_files(self, files_type, files):
        for file in files:
            # path =
            try:
                os.mkdir(os.path.join(settings.MEDIA_URL, 'projects', self.id, files_type))
            except:
                pass
            response = requests.get(file["from"], stream=True)
            with open(os.path.join(settings.MEDIA_URL, 'projects', self.id, files_type, file["to"]), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

        print(settings.BASE_DIR)


class Page(models.Model):
    id = models.CharField("Идентификатор", max_length=255, null=False, blank=False, primary_key=True)
    projectid = models.CharField("Проект", max_length=255, null=False, blank=False)
    title = models.CharField("Название", max_length=255, null=False, blank=False)
    descr = models.CharField("Описание", max_length=255, null=True, blank=True)
    img = models.CharField("Картинка", max_length=255, null=True, blank=True)
    featureimg = models.CharField("featureimg", max_length=255, null=True, blank=True)
    alias = models.CharField("alias", max_length=255, null=True, blank=True)
    date = models.CharField("Дата создания", max_length=255, null=True, blank=True)
    sort = models.CharField("Номер очередности в списке страниц", max_length=255, null=True, blank=True)
    published = models.CharField("Адрес страницы", max_length=255, null=True, blank=True)
    filename = models.CharField("Имя файла", max_length=255, null=True, blank=True)
    static_files = models.ManyToManyField('StaticFile', blank=True)
    # images = models.ManyToManyField('StaticFile')
    # css = models.ManyToManyField('StaticFile')
    # js = models.ManyToManyField('StaticFile')
    html = models.TextField("HTML", default="")


class StaticFile(models.Model):
    filename = models.CharField("Имя файла", max_length=255, null=False, blank=False)
    type = (('image', 'Картинка'), ('js', 'JavaScript-файл'), ('css', 'CSS-файл'))
    path = models.CharField("Путь у нас", max_length=255, null=False, blank=False)
    path_tilda = models.CharField("Путь у них", max_length=255, null=False, blank=False)
