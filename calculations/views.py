from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home.html")

def one_sample(request):
    return render(request, "one-sample.html")

def two_sample(request):
    return render(request, "two-sample.html")
