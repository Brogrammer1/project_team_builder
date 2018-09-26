from django.conf import settings
from django.db import models
from accounts.models import Skill


# Create your models here.


class Project(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="projects")
    title = models.CharField(max_length=140)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    time_line_description = models.TextField(default='')
    applicant_req = models.TextField(default='')

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=40)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE,
                              related_name='positions', )
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='positions', )
    filled = models.BooleanField(default=False)

    def __str__(self):
        return "{}-{}".format(self.title, self.project)


class Application(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE,
                                 related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='applications')
    status = models.CharField(max_length=30, default='processing')

    def __str__(self):
        return '{}-{} application'.format(self.position.position_title,
                                          self.candidate)
