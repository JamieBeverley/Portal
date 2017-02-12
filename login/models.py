from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


# Create your models here.

class Users(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=20)
	

	# def __init__(self, username, password):
	# 	self.username = username
	# 	self.password = password



  
SEX_CHOICES = (('m','Male'),('f','Female'),('mtf','MtF Female'),('ftm','FtM Male'),('oth','Other'))

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	isStudy= models.BooleanField(default=False)
	# This is kind of hacky: used so 'Profile' can be used both as a Research study criteria 
	# (like a fake person who meets all inclusion criteria), and as an actual profile.
	username = models.CharField(max_length=150, primary_key=True)
	dateOfBirth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
	height = models.IntegerField(null=True, blank = True, verbose_name = "Height (cm)", help_text="height in cm" )
	weight = models.IntegerField(null=True, blank = True, verbose_name = "Weight (kg)", help_text="weight in kilograms" )
	sex = models.CharField(max_length = 3, choices=SEX_CHOICES, null=True, blank=True, verbose_name = "Identified Sex")
	

	def isSimilar(self,other):
		return self.dateOfBirth==other.dateOfBirth and self.height==other.height and self.weight==other.weight and self.sex==other.sex

class Studies(models.Model):
	# of the form username/studyname
	creator = models.CharField(max_length=150)
	name = models.CharField(max_length=100, verbose_name="Name", primary_key=True)
	description = models.TextField(max_length=500, verbose_name= "Description")
	inclusion = models.TextField(verbose_name="Inclusion Criteria")
	exclusion = models.TextField(verbose_name="Exclusion Criteria")
	profile = models.OneToOneField( Profile, on_delete=models.CASCADE, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance,username=instance.username)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save

# 	criteria = models.ForeignKey('StudyCriteria')
# class StudyCriteria(models.Model):
# 	dateOfBirth = models.ForeignKey(CriteriaSpec)

# class CriteriaSpec(models.Model):
# 	"""Specify specific criteria for a study"""
# 	valType = (('Number','Number'),('y/n','y/n'),('Option','Option'))
# 	value = models.CharField(max_length=100)


# class Person():

# 	def __int__(self, name, age, height):
# 		self.name= name
# 		self.age = age
# 		self.height = height

# 	def changeName(self, name):
# 		self.name = name


# x = Person('Jamie', 21, 6)

# x.name
# x.age
# x.height

# x.changeName('Gali')