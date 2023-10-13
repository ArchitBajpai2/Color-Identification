# urine_strip/models.py
from django.db import models

class UrineStripImage(models.Model):
    image = models.ImageField(upload_to='images/')
    colors = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uploaded_at)
