from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def home(request):
    # return HttpResponse('Hello')  # return a string 'Hello'
    # return a html file (written in the templates/)
    return render(request, 'home.html', {'mes': 'Type some words in the box below'})

def eggs(request):
    # retunr html
    return HttpResponse('<h1>Eggs are great</h1>')


def count(request):
    fulltext = request.GET['fulltext']  # get the variables in the url (via GET request)
    wordlist = fulltext.split()
    words = len(wordlist)
    word_dict = {}
    for word in wordlist:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return render(request, 'count.html', {'fulltext': fulltext, 'words': words, 'word_dict': word_dict.items()})


def about(request):
    return render(request, 'about.html')


@login_required
def userhome(request):
    return render(request, "registration/success.html", {})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('userhome')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
