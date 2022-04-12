from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Recruiter)
admin.site.register(Candidate)
admin.site.register(Opening)
admin.site.register(Referral)