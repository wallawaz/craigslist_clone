from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.search}'

    class Meta:
        verbose_name_plural = "searches"

class Posting:
    """
    Simple class to contain Craigslist post data.
    """
    def __init__(self, url, title, image_url, price=None):
        self.url = url
        self.title = title
        self.image_url = image_url
        self.price = price 