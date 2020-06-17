from __future__ import unicode_literals

from django.db import models

class user(models.Model):
	user_id=models.CharField(max_length=30,default='',blank=True,null=True,unique=True)
	n = models.IntegerField(default=1)
	e = models.IntegerField(default=1)
	d = models.IntegerField(default=1)

	
	
