# Generated by Django 2.1 on 2018-09-03 14:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('export_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tildarequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tildarequest',
            name='pages',
            field=models.ManyToManyField(blank=True, to='export_app.Page'),
        ),
        migrations.AddField(
            model_name='tildarequest',
            name='projects',
            field=models.ManyToManyField(blank=True, to='export_app.Project'),
        ),
        migrations.AddField(
            model_name='tildarequest',
            name='publickey',
            field=models.CharField(default='5iusv518bgyj2ox69cpi', max_length=20),
        ),
        migrations.AddField(
            model_name='tildarequest',
            name='secretkey',
            field=models.CharField(default='wyf7n1weosiuacn6hoft', max_length=20),
        ),
    ]
