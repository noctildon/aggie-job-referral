from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Company(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True) # company name
    position=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=2000,null=True)
    Location=models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.name


class Candidates(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    dob=models.DateField(null=True)
    is_company=models.BooleanField(default=False)

    # username=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    USERNAME_FIELD = "username"
    def __str__(self):
        return self.name