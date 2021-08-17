from django.db import models

# Create your models here.
class feedback(models.Model):
    name=models.CharField(max_length=100)
    feedback=models.TextField()
    rate=models.IntegerField()
    def __str__(self):
        return self.name
