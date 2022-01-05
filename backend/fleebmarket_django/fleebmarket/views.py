from django.http import HttpResponseRedirect
from django.shortcuts import render


def redirect_search(request):
    return HttpResponseRedirect("/search/")


def about(request):
    return render(request, 'generic/about.html', {})

def contact(request):
    return render(request, 'generic/contact.html', {})
