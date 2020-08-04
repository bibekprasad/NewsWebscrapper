from django.db import models

# Create your models here.


class Link(models.Model):


	def __str__(self):
		return (str(self.Link_name))

	Link_address=models.CharField(max_length=1000,null=True,blank=True)
	Link_name=models.CharField(max_length=1000,null=True,blank=True)	
	Summary=models.TextField(max_length=5000,null=True,blank=True)
 