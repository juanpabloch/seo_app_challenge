from django.contrib.auth.models import AbstractUser  
from django.db import models  

class CustomUser(AbstractUser):  
	pass


class UrlData(models.Model):
    STRATEGY_CHOICES = [
		('desktop', 'Desktop'),
		('mobile', 'Mobile'),
	]

    url_1 = models.URLField()
    url_2 = models.URLField()
    strategy = models.CharField(max_length=10, choices=STRATEGY_CHOICES)
    index_1 = models.FloatField()
    interactive_1 = models.FloatField()
    index_2 = models.FloatField()
    interactive_2 = models.FloatField()

    def __str__(self):
        return f'{self.url_1} vs {self.url_2}'

    class Meta:
        db_table = "url_data"
        ordering = ["-id"]