from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    # return HttpResponse('Hello')  # return a string 'Hello'
    return render(request, 'home.html', {'mes': 'Type some words in the box below'})  # return a html file (written in the templates/)


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
