from django.db import models

class Foto(models.Model):

	image = models.URLField(blank=True, max_length=254)
	compass = models.IntegerField(blank=True)
	latitude = models.FloatField(blank=True)
	longitude = models.FloatField(blank=True)
	color = models.CharField(blank=True, default="256,256,256", max_length = 11)
	created_at = models.DateTimeField(auto_now_add=True)
