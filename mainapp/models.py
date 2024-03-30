from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# create database table
class Student(models.Model):
      # every student instance belong to a specific User
      user= models.ForeignKey(User, on_delete=  models.CASCADE)
      name= models.CharField(max_length=50)
      email= models.EmailField()
      age= models.IntegerField()
      gender= models.CharField(max_length=25)
      created_at= models.DateTimeField(auto_now_add = True)
# will return 
      def __str__(self):
            return f"{self.user.username},{self.name}"