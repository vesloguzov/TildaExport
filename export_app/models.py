# from time import gmtime
from django.db import models
import requests
import json


class TildaRequest(models.Model):
    request_count = models.IntegerField("Количество запросов за час", default=0)
    publickey = "ptjpckc4gc0feyrbgj0w"
    secretkey = "nil2glnhbg00skcx1"
    base_url = "http://api.tildacdn.info/v1/"

    def getprojectslist(self):
        if self.request_count < 120:
            # request = requests.get(f'{self.base_url}getprojectslist/?publickey={self.publickey}&secretkey={self.secretkey}')
            request = requests.get("{}getprojectslist/?publickey={}&secretkey={}".format(self.base_url, self.publickey, self.secretkey))
            response = json.loads(request.json())
            if response["status"] == "FOUND":
                for project in response["result"]:
                    project_object = Project.objects.get_or_create(id=project["id"])
                    project_object.update(title=project["title"], descr=project["descr"])
            self.request_count += 1


class StaticFile(models.Model):
    filename = models.CharField("Имя файла", max_length=255, null=False, blank=False)
    type = (('image', 'Картинка'), ('js', 'JavaScript-файл'), ('css', 'CSS-файл'))
    path = models.CharField("Путь у нас", max_length=255, null=False, blank=False)
    path_tilda = models.CharField("Путь у них", max_length=255, null=False, blank=False)


class Project(models.Model):
    id = models.CharField("Идентификатор", max_length=255, null=False, blank=False)
    title = models.CharField("Название", max_length=255, null=False, blank=False)
    descr = models.CharField("Описание", max_length=255, null=True, blank=True)
    customdomain = models.CharField("Домен", max_length=255, null=True, blank=True)
    export_csspath = models.CharField("Путь экспорта", max_length=255, null=True, blank=True)
    export_jspath = models.CharField("Путь экспорта", max_length=255, null=True, blank=True)
    export_imgpath = models.CharField("Путь экспорта", max_length=255, null=True, blank=True)
    indexpageid = models.CharField("indexpageid", max_length=255, null=True, blank=True)
    favicon = models.CharField("Картинка", max_length=255, null=True, blank=True)
    page404id = models.CharField("page404id", max_length=255, null=True, blank=True)
    images = models.ManyToManyField('StaticFile')
    js = models.ManyToManyField('StaticFile')
    css = models.ManyToManyField('StaticFile')
    ProjectPages = models.ManyToManyField('Page')


class Page(models.Model):
    id = models.CharField("Идентификатор", max_length=255, null=False, blank=False)
    projectid = models.CharField("Проект", max_length=255, null=False, blank=False)
    title = models.CharField("Название", max_length=255, null=False, blank=False)
    descr = models.CharField("Описание", max_length=255, null=False, blank=True)
    img = models.CharField("Картинка", max_length=255, null=False, blank=True)
    featureimg = models.CharField("featureimg", max_length=255, null=False, blank=True)
    alias = models.CharField("alias", max_length=255, null=False, blank=True)
    date = models.CharField("Дата создания", max_length=255, null=False, blank=True)
    sort = models.CharField("Номер очередности в списке страниц", max_length=255, null=False, blank=True)
    published = models.CharField("Адрес страницы", max_length=255, null=False, blank=True)
    filename = models.CharField("Имя файла", max_length=255, null=False, blank=False)
    images = models.ManyToManyField('StaticFile')
    css = models.ManyToManyField('StaticFile')
    js = models.ManyToManyField('StaticFile')
    html = models.TextField("HTML", default="")
