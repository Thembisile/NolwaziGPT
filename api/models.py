from django.db import models

class Documents(models.Model):
    file_name = models.CharField(max_length=255)
    content = models.BinaryField()
    collection_name = models.CharField(max_length=255)
