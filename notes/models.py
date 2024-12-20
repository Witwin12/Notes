import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Note (models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    content = models.TextField()
    file_path = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)