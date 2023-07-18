import pandas as pd
from .stats_calculations import calc_ttest1

from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "home.html")

def one_sample(request):

    if request.method == "POST":


        test = request.POST.get("test")
        alternative = request.POST.get("alternative")

        try:
            value = float(request.POST.get("value"))
            alpha = float(request.POST.get("alpha"))
        
        except:
            messages.add_message(request, messages.WARNING, "Value or alpha aren't numeric")
            return render(request, "one-sample.html", context={"calculationds" : False})

        file = request.FILES.get("data_file")
        
        try:
            df = pd.read_csv(file)

        except:
            messages.add_message(request, messages.WARNING, "Couldn't Open File")
            return render(request, "one-sample.html", context={"calculationds" : False})

        if test == "t":

            context = calc_ttest1(df, value, alternative, alpha)

            return render(request, "one-sample.html", context=context)



    return render(request, "one-sample.html", {"calculations" : False})

def two_sample(request):
    return render(request, "two-sample.html")
