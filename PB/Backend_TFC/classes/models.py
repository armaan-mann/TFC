import datetime as dt

from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from studios.models import Studio


class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.CharField(max_length=100)
    keywords = models.TextField()
    capacity = models.PositiveIntegerField()
    studio = models.ForeignKey(to=Studio, on_delete=models.CASCADE, blank=True, null=True)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    start_recursion = models.DateField(null=False, blank=False)
    end_recursion = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.start_recursion > self.end_recursion:
    #         raise ValidationError(
    #             {'start_recursion': "Start Recursion cannot exceed end_recursion"})
    #     if self.start_time > self.end_time:
    #         raise ValidationError(
    #             {'start_recursion': "Start Time cannot exceed End Time"})
    #
    #     self.full_clean()
    #     return super().save()

    def save(self, update_fields=False, **kwargs):
        # print(self, update_fields, kwargs)
        if not update_fields:
            start = self.start_recursion
            stop = self.end_recursion
            objects = []

            while start < stop:
                list_of_keywords = [i.lstrip(' ') for i in self.keywords.split(',')]
                _time = Class(name=self.name,
                              description=self.description,
                              coach=self.coach,
                              keywords=list_of_keywords,
                              capacity=self.capacity,
                              studio=self.studio,
                              start_time=self.start_time,
                              end_time=self.end_time,
                              start_recursion=self.start_recursion,
                              end_recursion=self.end_recursion)
                objects.append(_time)
                self.start_recursion = (self.start_recursion + dt.timedelta(days=7))
                start = self.start_recursion

            Class.objects.bulk_create(objects)
        else:
            # print("Updated fields", update_fields)
            Class.objects.filter(id=self.id).update(**update_fields)
            # Class.objects.filter(id=self.id).update(capacity=self.capacity)
            return



class Enrollment(models.Model):
    _user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    _enrolled = models.ForeignKey(to=Class, on_delete=models.CASCADE, default=None)
    _start_time = models.TimeField(null=True, blank=True)
    _start_recursion = models.DateField(null=True, blank=True)
    _enroll_or_drop = models.CharField(max_length=25, blank=False, null=True)
    _is_active = models.BooleanField(default=True, null=False, blank=False)


class ClassHistory(models.Model):
    User = models.ForeignKey(to=Enrollment, on_delete=models.CASCADE)
    Enrollment_Status = models.CharField(max_length=10, null=True, blank=True)
    Name = models.CharField(max_length=100)
    Coach = models.CharField(max_length=100)
    Keywords = models.TextField()
    Studio = models.ForeignKey(to=Studio, on_delete=models.CASCADE, blank=True, null=True)
    Start_Time = models.TimeField(null=False, blank=False)
    End_Time = models.TimeField(null=False, blank=False)
    Start_Recursion = models.DateField(null=False, blank=False)
    End_Recursion = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.Enrollment_Status
