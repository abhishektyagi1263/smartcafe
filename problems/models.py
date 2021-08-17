from django.db import models
from accounts.models import User

# Create your models here.


class problem_detail(models.Model):
    no=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    difficulty=models.CharField(max_length=100)
    info=models.CharField(max_length=100)
    que=models.TextField()
    input1=models.TextField()
    input2=models.TextField()
    output1=models.TextField()
    output2=models.TextField()

    def __str__(self):
        return self.name
class Response(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ass=models.ForeignKey(problem_detail,on_delete=models.CASCADE)
    submittion=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
    name=models.CharField(max_length=30)
    question=models.CharField(max_length=30)
    code=models.TextField()
    marks=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name
