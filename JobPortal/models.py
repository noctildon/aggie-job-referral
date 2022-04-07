from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True) # company name
    email = models.CharField(max_length=200,null=True)

    position=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=2000,null=True)
    Location=models.CharField(max_length=2000,null=True)
    USERNAME_FIELD = "username" # this line is necessary
    def __str__(self):
        return self.name


class Candidates(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    is_company=models.BooleanField(default=False)

    USERNAME_FIELD = "username" # this line is necessary
    def __str__(self):
        return self.name