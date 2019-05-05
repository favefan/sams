from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Student(models.Model):
    student_ID = models.BigIntegerField(unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=50, default='undef', null=False)
    sex = models.BooleanField(choices=((0, '男'), (1, '女')), default=0)
    department = models.PositiveSmallIntegerField(default=0)
    major = models.CharField(max_length=50, default='undef')
    enroll_year = models.PositiveSmallIntegerField(default=0000)
    schooling_year = models.PositiveSmallIntegerField(default=4)
    # system_password = models.CharField(max_length=300, default='000000')

    def __str__(self):
        return self.name

class User(AbstractUser):
    account = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

class Activity(models.Model):
    activity_ID = models.AutoField(unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=200, default='undef', null=False)
    introduction = models.CharField(max_length=300)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE) #, on_delete=models.CASCADE
    create_date = models.DateTimeField(default=timezone.now)
    capacity = models.PositiveSmallIntegerField(default=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

# class Organizer(models.Model):
#     system_ID = models.IntegerField(unique=True, null=False, primary_key=True)
#     name = models.CharField(max_length=200, default='AnymousOrganizer')
#     system_password = models.CharField(max_length=300, default='000000')

#     def __str__(self):
#         return self.name

class Entrylist(models.Model):
    entry_no = models.AutoField(unique=True, null=False, primary_key=True)
    student = models.ForeignKey(Student, null=False, on_delete=models.CASCADE) #, on_delete=models.CASCADE
    activity = models.ForeignKey(Activity, null=False, on_delete=models.CASCADE) #, on_delete=models.CASCADE
    entry_date = models.DateTimeField(default=timezone.now)
    awards = models.CharField(max_length=200, null=True, blank=True)
    score_kind = models.CharField(max_length=100, null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0, null=True, blank=True)

