from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class userlog(models.Model):
	userid = models.CharField(max_length=200,null=True)
	passwd = models.CharField(max_length=200,null=True)
	def __str__(self):
		return self.userid + ' ' + self.passwd
class usercr(models.Model):
	firstnm = models.CharField(max_length=200,null=True)
	lastnm = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)
	userid = models.CharField(max_length=200,null=True)
	passwd = models.CharField(max_length=200,null=True)
	def __str__(self):
		return self.userid + ' ' + self.passwd+' '+ self.firstnm + ' ' + self.lastnm+ ' ' + self.email