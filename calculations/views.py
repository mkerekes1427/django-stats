import pandas as pd
from .stats_calculations import calc_ttest1, calc_ztest1, calc_prop1

from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "home.html")

def one_sample(request):

    if request.htmx: 
        
        if request.GET.get("test") == "prop":
            return render(request, "partials/propform.html", {"calculations" : False})
        
        return render(request, "partials/tz_form.html", {"calculations" : False})
    
    

    if request.method == "POST":


        test = request.POST.get("test")
        alternative = request.POST.get("alternative")

        try:
            value = float(request.POST.get("value"))
            alpha = float(request.POST.get("alpha"))
        
        except:
            messages.add_message(request, messages.WARNING, "Value or alpha aren't numeric")
            return render(request, "one-sample.html", context={"calculations" : False})

        # If the test is not a proportion test, read the file in.
        if test != "prop":

            file = request.FILES.get("data_file")
            
            try:
                df = pd.read_csv(file)

            except:
                messages.add_message(request, messages.WARNING, "Couldn't Open File")
                return render(request, "one-sample.html", context={"calculations" : False})

        if test == "t":

            try:
                context = calc_ttest1(df, value, alternative, alpha)
            except:
                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}
        
        elif test == "z":
            
            try:
                context = calc_ztest1(df, value, alternative, alpha)
            except:
                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}
        
        else:

            method = request.POST.get("method")

            try:
                successes = int(request.POST.get("successes"))
                trials = int(request.POST.get("trials"))

            except:
                
                messages.add_message(request, messages.WARNING, "Successes or trials aren't integers")
                context = {"calculations" : False}

                return render(request, "one-sample.html", context=context)

            try:
                context = calc_prop1(successes, trials, value, alternative, alpha, method)

            except:

                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}
            
        return render(request, "one-sample.html", context=context)


    return render(request, "one-sample.html", {"calculations" : False})

def two_sample(request):

    if request.htmx:

        if request.GET.get("test") in ["ind-t", "ind-z", "pair-t", "pair-z", "tukey"]:
            return render(request, "partials/tz2_form.html", {"calculations" : False})
        
        return render(request, "partials/propform.html", {"calculations" : False})

    return render(request, "two-sample.html", {"calculations" : False})
