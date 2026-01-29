from django.db import models

# Professor model
class Professor(models.Model):
    Name = models.CharField(max_length=100, null=True)

class Course(models.Model):
    CourseNumber = models.IntegerField(blank=True, null=True)
    Honors = models.BooleanField(blank=True, null=True)
    Subject = models.CharField(max_length=4, null=True, blank=True)
    MeetingDays = models.CharField(max_length=50, null=True, blank=True)
    PassRate = models.FloatField(max_length=3, blank=True, null=True)
    StartTime = models.CharField(max_length=10, blank=True, null=True) 
    EndTime = models.CharField(max_length=10, blank=True, null=True)
    