from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.forms.models import model_to_dict
from django.http import FileResponse, Http404
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import *


def home(request):
    if request.user.is_authenticated:
        candidate_login = Candidate.objects.filter(user=request.user)
        recruiter_login = Recruiter.objects.filter(user=request.user)


        ###################### Candidate session ######################
        if candidate_login:
            candidate = candidate_login[0]
            openings = Opening.objects.all()

            # Filter the openings that the candidate has applied
            openings_ = []
            for opening in openings:
                requested_refs_for_opening = Referral.objects.filter(applicant=request.user).filter(opening=opening)
                pk = opening.pk

                # Convert to dict
                ref_opening = model_to_dict(opening)
                ref_opening['pk'] = pk
                if requested_refs_for_opening:
                    ref_opening['ref_status'] = requested_refs_for_opening[0].status
                else:
                    ref_opening['ref_status'] = 'new'
                openings_.append(ref_opening)

            context = {'candidate': candidate, 'openings': openings_}
            return render(request,'candidate_home.html',context)
        ###############################################################


        ###################### Recruiter session ######################
        if recruiter_login:
            recruiter = recruiter_login[0]
            openings = Opening.objects.filter(recruiter=request.user)

            openings_ = []
            for opening in openings:
                refs = Referral.objects.filter(opening=opening)
                pk = opening.pk

                # Convert to dict
                opening = model_to_dict(opening)
                opening['refs'] = refs
                opening['pk'] = pk
                openings_.append(opening)

            context = {'recruiter': recruiter, 'openings': openings_ }
            return render(request,'hr.html',context)
        ###############################################################

    else:
        openings = Opening.objects.all()
        context = {'openings': openings }
        return render(request,'Jobseeker.html',context)


# Dashboard
def Dashboard(request):
    if request.user.is_authenticated:
        candidate_login = Candidate.objects.filter(user=request.user)
        recruiter_login = Recruiter.objects.filter(user=request.user)

        ###################### Candidate session ######################
        if candidate_login:
            candidate = candidate_login[0]

            initial = {'resume': candidate.resume, 'email_notification': candidate.email_notification}
            form = DashboardFormCandidate(initial=initial)
            if request.method == 'POST':
                form = DashboardFormCandidate(request.POST,request.FILES)
                if form.is_valid():
                    candidate.resume, candidate.email_notification = form.save()
                    candidate.save()

                    return redirect('home')

            context = {'user': candidate, 'form': form}
            return render(request,'dashboard.html', context)
        ###############################################################

        ###################### Recruiter session ######################
        if recruiter_login:
            recruiter = recruiter_login[0]

            initial = {'email_notification': recruiter.email_notification}
            form = DashboardFormRecruiter(initial=initial)

            if request.method == 'POST':
                form = DashboardFormRecruiter(request.POST,request.FILES)
                if form.is_valid():
                    recruiter.email_notification = form.save()
                    recruiter.save()
                    return redirect('home')

            context = {'user': recruiter, 'form': form}
            return render(request,'dashboard.html', context)
        ###############################################################

    return redirect('home')


# View the applicants' requests
def hrApplicants(request):
    if request.user.is_authenticated:
        recruiter_login = Recruiter.objects.filter(user=request.user)
        if recruiter_login:
            recruiter = recruiter_login[0]
            opening_id = request.GET['openingid']


            # Marking the referral 'processed'
            try:
                ref_id = request.GET['refid']
                ref = Referral.objects.get(pk=ref_id)
                ref.status = 'processed'
                ref.save()

                # sending email notification
                candidate_user = ref.applicant
                candidate = Candidate.objects.get(user=candidate_user)
                send_email2candidate(candidate)
            except:
                pass

            # Collect the referrals
            opening = Opening.objects.get(pk=opening_id)
            refs = Referral.objects.filter(opening=opening)

            refs_ = []
            for ref in refs:
                applicant = ref.applicant
                candidate = Candidate.objects.get(user=applicant)
                applicant_name = candidate.name
                applicant_email = candidate.email

                ref_ = model_to_dict(ref)
                ref_['app_name'] = applicant_name
                ref_['app_email'] = applicant_email
                ref_['pk'] = ref.pk
                refs_.append(ref_)

            context = {'recruiter': recruiter, 'refs': refs_, 'opening': opening}
            return render(request,'hr_applicants.html', context)
    return redirect('home')


# Edit the opening
def Edit(request):
    if request.user.is_authenticated:
        recruiter_login = Recruiter.objects.filter(user=request.user)
        if recruiter_login:
            opening_id = request.GET.get('openingid')
            opening = Opening.objects.get(pk=opening_id)

            initial = {'company': opening.company, 'job_title': opening.job_title, 'job_description': opening.job_description, 'status': opening.status}
            form = EditForm(initial=initial)
            if request.method == 'POST':
                form = EditForm(request.POST,request.FILES)
                if form.is_valid():
                    opening.company, opening.job_title, opening.job_description, opening.status = form.save()
                    opening.save()

                    return redirect('home')

            context = {'form': form}
            return render(request,'edit.html',context)

    return redirect('home')


def pdf_view(request):
    try:
        link =  request.GET.get('link')
        return FileResponse(open('media/'+link, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


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
                Candidate.objects.create(user=currUser,name=name,email=currUser.email)
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
        context = {'form': Form, 'role': 'Recruiter/Empolyee'}
        return render(request,'register.html',context)


# Post opening
def PostPage(request):
    if request.user.is_authenticated:
        recruiter_login = Recruiter.objects.filter(user=request.user)
        if recruiter_login:
            form = PostForm()
            if request.method == 'POST':
                form = PostForm(request.POST,request.FILES)
                if form.is_valid():
                    company, job_title, job_description = form.save()

                    Opening.objects.create(recruiter=request.user, company=company, job_title=job_title, job_description=job_description)
                    return redirect('home')
            context = {'form': form}
            return render(request,'post.html',context)

    return redirect('home')


# Request referral
def RequestPage(request):
    if request.user.is_authenticated:
        candidate_login = Candidate.objects.filter(user=request.user)
        if candidate_login:
            candidate = candidate_login[0]

            initial = {'resume': candidate.resume}
            form = RequestForm(initial=initial)

            opening_id = request.GET.get('openingid')
            opening = Opening.objects.get(pk=opening_id)
            if request.method == 'POST':
                form = RequestForm(request.POST,request.FILES)
                if form.is_valid():
                    app_info, resume = form.save()
                    Referral.objects.create(applicant=request.user,opening=opening, app_info=app_info, resume=resume)

                    recruiter_user = opening.recruiter
                    recruiter = Recruiter.objects.get(user=recruiter_user)
                    send_email2recruiter(recruiter)
                    return redirect('home')
            context = {'form': form}
            return render(request,'request_ref.html',context)

    return redirect('home')



def send_email2recruiter(recruiter, testing=True):
    if not recruiter.email_notification:
        return

    subject = 'A referral request is submitted.'
    message = f'Dear {recruiter.name},\nThere is recently new referral request. Please check the AJR website.'

    if testing:
        print('subject', subject)
        print('message', message)
        print('email to', recruiter.email)
        return

    send_mail(subject, message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recruiter.email],
        fail_silently=False)



def send_email2candidate(candidate, testing=True):
    if not candidate.email_notification:
        return

    subject = 'Your referral request gets processed!!'
    message = f'Dear {candidate.name},\nYour referral request gets processed!! Wait for more from the recruiter.'

    if testing:
        print('subject', subject)
        print('message', message)
        print('email to', candidate.email)
        return

    send_mail(subject, message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[candidate.email],
        fail_silently=False)