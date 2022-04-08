from django.db import models
from django.contrib.auth.models import User


class Recruiter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True) # recruiter name
    email = models.CharField(max_length=200,null=True)

    USERNAME_FIELD = "username" # this line is necessary
    def __str__(self):
        return self.name


# TODO: add applicants field
class Jobs(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200,null=True)
    company = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.job_title


class Candidates(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    USERNAME_FIELD = "username" # this line is necessary
    def __str__(self):
        return self.name