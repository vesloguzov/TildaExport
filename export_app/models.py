# from time import gmtime
from django.db import models
import requests
from django.conf import settings
from binaryornot.check import is_binary
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
                # print("id", response["result"]["id"])
                project.id = response["result"]["id"]
                project.title = response["result"]["title"]
                project.descr = response["result"]["descr"]
                project.customdomain = response["result"]["customdomain"]
                project.export_csspath = response["result"]["export_csspath"]
                project.export_jspath = response["result"]["export_jspath"]
                project.export_imgpath = response["result"]["export_imgpath"]
                project.indexpageid = response["result"]["indexpageid"]
                project.save()
                if "js" in response["result"].keys():
                    project.save_static_files('js', response["result"]["js"])
                if "css" in response["result"].keys():
                    project.save_static_files('css', response["result"]["css"])
                if "images" in response["result"].keys():
                    project.save_static_files('images', response["result"]["images"])


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

    def getpagefullexport(self, project_id, page_id):
        if self.request_count < self.requests_limit:
            request = requests.get(
                "{}getpagefullexport/?publickey={}&secretkey={}&pageid={}".format(self.base_url, self.publickey,
                                                                                  self.secretkey, page_id))
            self.increment()
            response = request.json()
            print(response)
            if response["status"] == "FOUND":
                print("id", response["result"]["id"])
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
                page_object.html = page["html"]
                page_object.save()
                if "images" in response["result"].keys():
                    page_object.save_page_images(response["result"]["images"])
                page_object.save_html_file()

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
            path = os.path.join(settings.MEDIA_ROOT, 'projects', self.id)
            newfile = os.path.join(settings.MEDIA_ROOT, 'projects', self.id, file["to"])
            if not os.path.isdir(path):
                os.mkdir(path)
            response = requests.get(file["from"], stream=True)
            with open(newfile, 'w') as out_file:
                out_file.write(response.text)


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
    page_path = models.CharField("Адрес страницы на сервере", max_length=255, null=True, blank=True)

    def save_html_file(self):
        path = os.path.join(settings.MEDIA_ROOT, 'projects', self.projectid)
        newfile = os.path.join(settings.MEDIA_ROOT, 'projects', self.projectid, self.filename)
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(newfile, 'w') as out_file:
            out_file.write(self.html)
        # print("newfile", newfile)
        self.page_path = os.path.join(settings.MEDIA_URL, 'projects', self.projectid, self.filename)
        self.save()

    def save_page_images(self, files):
        for file in files:
            path = os.path.join(settings.MEDIA_ROOT, 'projects', self.projectid)
            newfile = os.path.join(settings.MEDIA_ROOT, 'projects', self.projectid, file["to"])
            if not os.path.isdir(path):
                os.mkdir(path)
            response = requests.get(file["from"], stream=True)
            print("is_binary(): ", newfile, is_binary(newfile))
            if is_binary(newfile):
                with open(newfile, 'wb') as out_file:
                    for chunk in response:
                        out_file.write(chunk)
            else:
                with open(newfile, 'w') as out_file:
                    out_file.write(response.text)


class StaticFile(models.Model):
    filename = models.CharField("Имя файла", max_length=255, null=False, blank=False)
    type = (('image', 'Картинка'), ('js', 'JavaScript-файл'), ('css', 'CSS-файл'))
    path = models.CharField("Путь у нас", max_length=255, null=False, blank=False)
    path_tilda = models.CharField("Путь у них", max_length=255, null=False, blank=False)
