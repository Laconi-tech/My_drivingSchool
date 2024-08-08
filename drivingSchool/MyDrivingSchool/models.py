from django.db import models
from django.contrib.auth.models import User, Group

# DateField
# DateTimeField
# EmailField

class Users(models.Model):
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    username = models.CharField(max_length = 22, unique = True)
    email = models.EmailField(max_length = 35, unique = True)
    password = models.CharField(max_length = 35)
    role = models.IntegerField(default = 1)

    def __str__(self):
        return self.username

class Planning(models.Model):
    rdv_stutent = models.CharField(max_length = 35)
    rdv_instructor = models.CharField(max_length = 35)
    rdv_date = models.DateTimeField()

    def __str__(self):
        return self.rdv_date
    
class My_Planning(models.Model):
    rdv_date = models.DateTimeField()
    title = models.CharField(max_length = 45)
    rdv_member = models.ManyToManyField(User, related_name='planning_hours')

    def __str__(self):
        return self.title
    
class UserMyPlanning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_planning = models.ForeignKey(My_Planning, on_delete=models.CASCADE)