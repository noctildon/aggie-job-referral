from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.forms.models import model_to_dict
from .models import *
from .forms import *


def home(request):
    if request.user.is_authenticated:

        candidate_login = Candidates.objects.filter(user=request.user)
        recruiter_login = Recruiter.objects.filter(user=request.user)

        if candidate_login:
            candidate = candidate_login[0]
            jobs = Jobs.objects.all()

            # apply the job
            jobid = request.GET.get('jobid')
            job_applying = jobs.filter(pk=jobid)
            if job_applying:
                job_applying = job_applying[0]
                job_applying.applicants.add(candidate)
                candidate.applied_jobs.add(job_applying)

            # filter the jobs that the candidate has applied
            applied_jobs_id = [j.pk for j in candidate.applied_jobs.all()]
            jobs = [model_to_dict(job) for job in jobs]
            for job in jobs:
                if job['job_id'] in applied_jobs_id:
                    job['status'] = 'applied'
                else:
                    job['status'] = 'new'

            context = {'candidate': candidate, 'jobs': jobs}
            return render(request,'candidate_home.html',context)


        if recruiter_login:
            recruiter = recruiter_login[0]
            jobs = Jobs.objects.filter(recruiter=request.user)
            for job in jobs:
                job.apps = job.applicants.all()

            context = {'recruiter': recruiter, 'jobs': jobs }

            return render(request,'hr.html',context)

    else:
        jobs = Jobs.objects.all()
        context = {
            'jobs': jobs,
        }
        return render(request,'Jobseeker.html',context)


def hrApplicants(request):
    if request.user.is_authenticated:
        recruiter_login = Recruiter.objects.filter(user=request.user)
        if recruiter_login:
            recruiter = recruiter_login[0]
            jobid = request.GET.get('jobid')

            job = Jobs.objects.filter(recruiter=request.user).filter(pk=jobid)[0]
            applicants = job.applicants.all()
            context = {'recruiter': recruiter, 'applicants': applicants}

            return render(request,'hr_applicants.html', context)

    return redirect('home')


def logoutUser(request):
    logout(request)
    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                return redirect('home')
        return render(request,'login.html')


# Candidate registration
def registerCandidate(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        Form = CandidateCreationForm()
        if request.method == 'POST':
            Form = CandidateCreationForm(request.POST)
            if Form.is_valid():
                currUser, name = Form.save()
                Candidates.objects.create(user=currUser,name=name,email=currUser.email)
                return redirect('login')
        context = {'form': Form, 'role': 'Candidate'}
        return render(request,'register.html',context)


# Recruiter registration
def registerRecruiter(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        Form = RecruiterCreationForm()
        if request.method == 'POST':
            Form = RecruiterCreationForm(request.POST)
            if Form.is_valid():
                currUser, name = Form.save()
                Recruiter.objects.create(user=currUser,name=name, email=currUser.email)
                return redirect('login')
        context = {'form': Form, 'role': 'Recruiter'}
        return render(request,'register.html',context)


def PostPage(request):
    if request.user.is_authenticated:
        recruiter_login = Recruiter.objects.filter(user=request.user)
        if recruiter_login:
            form = PostForm()
            if request.method == 'POST':
                form = PostForm(request.POST,request.FILES)
                if form.is_valid():
                    job_title, company, location = form.save()
                    Jobs.objects.create(recruiter=request.user, job_title=job_title, company=company, location=location)
                    return redirect('home')
            context = {'form': form}
            return render(request,'post.html',context)

    return redirect('home')