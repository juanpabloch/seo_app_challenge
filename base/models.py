from django.contrib.auth.models import AbstractUser  
from django.db import models  

class CustomUser(AbstractUser):  
	pass


class UrlData(models.Model):
    STRATEGY_CHOICES = [
		('desktop', 'Desktop'),
		('mobile', 'Mobile'),
	]

    url = models.URLField()
    strategy = models.CharField(max_length=10, choices=STRATEGY_CHOICES)
    index = models.FloatField()
    interactive = models.FloatField()

    def __str__(self):
        return self.url


class UrlCompareHistory(models.Model):
    url_1 = models.ForeignKey(UrlData, on_delete=models.CASCADE, related_name='compare_url_1')
    url_2 = models.ForeignKey(UrlData, on_delete=models.CASCADE, related_name='compare_url_2')

