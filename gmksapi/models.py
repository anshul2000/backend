from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

districts = {
    ('Paschim Medinipur','Paschim Medinipur'),
    ('Bankura','Bankura'),
    ('Jhargram','Jhargram'),
    ('Purlia','Purlia'),
    ('Birbhum','Birbhum'),
    ('General','General')
}
class Data(models.Model):
    id = models.AutoField(primary_key=True)
    loc= models.CharField(max_length=30, choices=districts)
    language= models.CharField(max_length=4, choices=[("en","English"), ("bn", "Bengali")])
    category=models.CharField(max_length=30)
    upload = models.FileField(blank=True, null=True)

    def __str__(self):
        return str(self.loc+"_"+self.category+"_"+self.language)

class UserContact(models.Model):
    number= models.IntegerField(blank=True,null=True,unique=True)
    def __str__(self):
        return str(self.number)

class Text(models.Model):
    text= models.CharField(blank=True,null=True,max_length=10000)
    def __str__(self):
        return str(self.text)

# Create your models here.

class Awareness(models.Model):
    id = models.AutoField(primary_key=True)
    event= models.CharField(max_length=1000)
    date=models.DateField()
    time=models.TimeField()
    loc= models.CharField(max_length=300)
    file=models.FileField(blank=True, null=True)
    def __str__(self):
        return str(self.event)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    district = models.CharField(max_length=30, choices=districts)

    def __str__(self):
        return str(f'Content: {self.content}, District: {self.district}')
