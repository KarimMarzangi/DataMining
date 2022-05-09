from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    image_article = models.TextField()
    content = models.CharField(max_length=5000)
    numview = models.IntegerField(max_length=200)