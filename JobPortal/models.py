from django.db import models
from django.contrib.auth.models import User
from model_utils.fields import StatusField
from model_utils import Choices


# aka employee
class Recruiter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    email_notification = models.BooleanField(default=False)

    USERNAME_FIELD = "username" # this line is necessary
    def __str__(self):
        return self.name

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    # applied_jobs = models.ManyToManyField('Job', through=Jobs.applicants.through, blank=True)
    resume = models.FileField(null=True) # PDF
    email_notification = models.BooleanField(default=False)


    USERNAME_FIELD = "username" # this line is necessary
    def __str__(self):
        return self.name


class Opening(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    company = models.CharField(max_length=200, null=True)
    job_title = models.CharField(max_length=200,null=True)
    job_description = models.CharField(max_length=200,null=True)
    status = StatusField(choices_name='OPENING_STATUS')

    OPENING_STATUS = Choices('open', 'close')
    def __str__(self):
        return self.job_title


class Referral(models.Model):
    applicant = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE)
    app_info = models.CharField(max_length=200, null=True) # eg. job title, id, link, descripion, and self-intro, etc
    resume = models.FileField(null=True) # PDF
    status = StatusField(choices_name='REFERRAL_STATUS')

    REFERRAL_STATUS = Choices('unprocessed', 'processed')
    def __str__(self):
        return self.applicant.name


# class Job(models.Model):
#     recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
#     job_title = models.CharField(max_length=200,null=True)
#     job_id = models.BigAutoField(primary_key=True)
#     company = models.CharField(max_length=200,null=True)
#     location = models.CharField(max_length=200,null=True)
#     applicants = models.ManyToManyField('Candidate', blank=True)

#     def __str__(self):
#         return self.job_title