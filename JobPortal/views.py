from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from .forms import *


def home(request):
    if request.user.is_authenticated:

        candidate_login = Candidates.objects.filter(user=request.user)
        if candidate_login:
            candidate = candidate_login[0]
            companies = Company.objects.all()
            context = {'candidate': candidate, 'companies':companies}
            return render(request,'candidate_home.html',context)

        candidates = Candidates.objects.all()
        context = {
            'candidates':candidates,
        }

        return render(request,'hr.html',context)

    else:
        companies = Company.objects.all()
        context = {
            'companies':companies,
        }
        return render(request,'Jobseeker.html',context)


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
                currUser, is_company, name = Form.save()
                Candidates.objects.create(user=currUser,name=name,email=currUser.email)
                return redirect('login')
        context = {'form': Form}
        return render(request,'register.html',context)


# Company registration
def registerCompany(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        # Form = UserCreationForm()
        Form = CompanyCreationForm()
        if request.method == 'POST':
            Form = CompanyCreationForm(request.POST)
            if Form.is_valid():
                currUser, name = Form.save()
                Company.objects.create(user=currUser,name=name, email=currUser.email)
                return redirect('login')
        context = {'form': Form}
        return render(request,'register.html',context)


def applyPage(request):
    form = ApplyForm()
    if request.method == 'POST':
        form = ApplyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'apply.html',context)