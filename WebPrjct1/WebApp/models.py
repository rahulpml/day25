from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class course(models.Model):
    #course = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=225)
    fee = models.IntegerField()

    def __str__(self):
        return self.course_name

class student(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE, null=True)
    std_name =models.CharField(max_length=225)
    std_address =models.CharField(max_length=225)
    std_age =models.IntegerField()
    Join_date =models.DateField()

    def __str__(self):
        return self.std_name

# course=course.objects.all()
# students=students.objects.all()
# crse=course.objects.get(course_name="BCA")
# cid=crse.id

# {% for i in course %}
# {% if i.id==cid %}
# {% for j in students %}
# {% if j.course_id==cid %}
# {{ j.std_name }}

#def __str__(self):
 #       return self.title

