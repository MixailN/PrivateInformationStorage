from django.db import models

# Create your models here.


class Page(models.Model):
    image = models.ImageField(upload_to='images/', null=True)
    password = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    visits_count = models.IntegerField()
