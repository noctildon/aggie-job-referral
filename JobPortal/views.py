from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import FileResponse, Http404
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
                requested_refs_for_opening = Referral.objects.filter(applicant=candidate).filter(opening=opening)

                # Convert to dict
                opening_ = model_to_dict(opening)
                opening_['pk'] = opening.pk
                if requested_refs_for_opening:
                    opening_['ref_status'] = requested_refs_for_opening[0].status
                else:
                    opening_['ref_status'] = 'new'
                openings_.append(opening_)

            context = {'candidate': candidate, 'openings': openings_}
            return render(request,'candidate_home.html',context)
        ###############################################################


        ###################### Recruiter session ######################
        if recruiter_login:
            recruiter = recruiter_login[0]
            openings = Opening.objects.filter(recruiter=recruiter)

            openings_ = []
            for opening in openings:
                refs = Referral.objects.filter(opening=opening)

                # Convert to dict
                opening_ = model_to_dict(opening)
                opening_['refs'] = refs
                opening_['pk'] = opening.pk
                openings_.append(opening_)

            context = {'recruiter': recruiter, 'openings': openings_ }
            return render(request,'hr.html',context)
        ###############################################################

    else:
        openings = Opening.objects.all()
        context = {'openings': openings }
        return render(request,'Jobseeker.html',context)


# Check if the new email is registered by someone other than the user
def duplicate_email_checking(new_email, user):
    new_email_user = User.objects.filter(email=new_email)
    if new_email_user:
        if new_email_user[0] != user:
            return True
    return False


# Dashboard for changing user settings, profile, etc
def Dashboard(request):
    if request.user.is_authenticated:
        candidate_login = Candidate.objects.filter(user=request.user)
        recruiter_login = Recruiter.objects.filter(user=request.user)

        ###################### Candidate session ######################
        if candidate_login:
            candidate = candidate_login[0]

            initial = {'resume': candidate.resume, 'email':candidate.email, 'email_notification': candidate.email_notification}
            form = DashboardFormCandidate(initial=initial)
            info_mesg = 'Please note that your resume may be accessible to anyone.'
            err_mesg = ''
            if request.method == 'POST':
                form = DashboardFormCandidate(request.POST,request.FILES,initial=initial)
                if form.is_valid():
                    candidate.resume, new_email, candidate.email_notification = form.save()

                    if duplicate_email_checking(new_email, request.user):
                        err_mesg = f'The email "{new_email}" has been registered by someone else. Please choose another email.'
                    else:
                        candidate.email = new_email
                        candidate.save()

                        mesg = 'Updates sucessfully saved'
                        context = {'mesg': mesg}
                        return render(request, 'confirm.html', context)

            context = {'user': candidate, 'form': form, 'err_mesg': err_mesg, 'info_mesg': info_mesg}
            return render(request,'dashboard.html', context)
        ###############################################################

        ###################### Recruiter session ######################
        if recruiter_login:
            recruiter = recruiter_login[0]

            initial = {'email':recruiter.email, 'email_notification': recruiter.email_notification}
            form = DashboardFormRecruiter(initial=initial)
            err_mesg = ''
            if request.method == 'POST':
                form = DashboardFormRecruiter(request.POST,request.FILES,initial=initial)
                if form.is_valid():
                    new_email, recruiter.email_notification = form.save()
                    if duplicate_email_checking(new_email, request.user):
                        err_mesg = f'The email "{new_email}" has been registered by someone else. Please choose another email.'
                    else:
                        recruiter.email = new_email
                        recruiter.save()
                        return redirect('home')

            context = {'user': recruiter, 'form': form, 'err_mesg': err_mesg}
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

                # sending email notification to candidate
                sendEmail2candidate(ref.applicant)
            except:
                pass

            # Collect the referrals
            opening = Opening.objects.get(pk=opening_id)
            refs = Referral.objects.filter(opening=opening)

            refs_ = []
            for ref in refs:
                ref_ = model_to_dict(ref)
                ref_['app_name'] = ref.applicant.name
                ref_['app_email'] = ref.applicant.email
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
                form = EditForm(request.POST,request.FILES,initial=initial)
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
        err_mesg = ''
        if request.method == 'POST':
            Form = CandidateCreationForm(request.POST)
            if Form.is_valid():
                try:
                    currUser, name = Form.save()
                    Candidate.objects.create(user=currUser,name=name,email=currUser.email)
                    return redirect('login')
                except ValidationError as e:
                    err_mesg = '; '.join(e.messages)
        context = {'form': Form, 'role': 'Candidate', 'err_mesg': err_mesg}
        return render(request,'register.html',context)


# Recruiter registration
def registerRecruiter(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        Form = RecruiterCreationForm()
        err_mesg = ''
        if request.method == 'POST':
            Form = RecruiterCreationForm(request.POST)
            if Form.is_valid():
                try:
                    currUser, name = Form.save()
                    Recruiter.objects.create(user=currUser,name=name, email=currUser.email)
                    return redirect('login')
                except ValidationError as e:
                    err_mesg = '; '.join(e.messages)
        context = {'form': Form, 'role': 'Recruiter/Empolyee', 'err_mesg': err_mesg}
        return render(request,'register.html',context)


# Post opening
def PostPage(request):
    if request.user.is_authenticated:
        recruiter_login = Recruiter.objects.filter(user=request.user)
        if recruiter_login:
            recruiter = recruiter_login[0]
            form = PostForm()
            if request.method == 'POST':
                form = PostForm(request.POST,request.FILES)
                if form.is_valid():
                    company, job_title, job_description = form.save()

                    Opening.objects.create(recruiter=recruiter, company=company, job_title=job_title, job_description=job_description)
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
                form = RequestForm(request.POST,request.FILES,initial=initial)
                if form.is_valid():
                    app_info, resume = form.save()
                    Referral.objects.create(applicant=candidate,opening=opening, app_info=app_info, resume=resume)

                    sendEmail2recruiter(opening.recruiter)
                    return redirect('home')
            context = {'form': form}
            return render(request,'request_ref.html',context)

    return redirect('home')


def ChangePwd(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(user=request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                mesg = 'Password sucessfully changed'
                context = {'mesg': mesg}
                return render(request, 'confirm.html', context)

        context = {'form': form}
        return render(request,'change_pwd.html', context)

    return redirect('home')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = \
    """We've emailed you instructions for re-setting your password.
        If an account exists with the email you entered. You should receive an email shortly.
        If you don't receive, please make sure you entered the address you registered with, and also check your spam folder."""
    success_url = reverse_lazy('password_reset_done')


def sendEmail2recruiter(recruiter):
    subject = 'A referral request is submitted.'
    message = f'Dear {recruiter.name},\nThere is recently new referral request. Please check the AJR website.'

    if recruiter.email_notification and settings.EMAIL_NOTIF:
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recruiter.email], fail_silently=False)
        return

    print('subject:', subject)
    print('message:', message)
    print('email to', recruiter.email)


def sendEmail2candidate(candidate):
    subject = 'Your referral request gets processed!!'
    message = f'Dear {candidate.name},\nYour referral request gets processed!! Wait for more from the recruiter.'

    if candidate.email_notification and settings.EMAIL_NOTIF:
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER,
            recipient_list=[candidate.email], fail_silently=False)
        return

    print('subject:', subject)
    print('message:', message)
    print('email to', candidate.email)