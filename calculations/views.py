import pandas as pd
from .stats_calculations import calc_ttest1, calc_ztest1, calc_prop1, calc_ttest2, calc_ztest2, calc_prop2, calc_mcnemar, calc_tukey

from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "home.html")

def one_sample(request):

    if request.htmx and request.method == "GET": 
        
        if request.GET.get("test") == "prop":
            return render(request, "partials/propform.html", {"calculations" : False})
        
        return render(request, "partials/tz_form.html", {"calculations" : False})
    

    if request.method == "POST":

        template = "one-sample.html"

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
                template = "partials/ttest_1.html"
            except:
                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}
        
        elif test == "z":
            
            try:
                context = calc_ztest1(df, value, alternative, alpha)
                template = "partials/ztest_1.html"
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
                template = "partials/prop1.html"

            except:

                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}
            
        return render(request, template, context=context)


    return render(request, "one-sample.html", {"calculations" : False})

def two_sample(request):

    if request.htmx and request.method == "GET":

        if request.GET.get("test") in ["ind-t", "ind-z"]:
            return render(request, "partials/tz2_form.html", {"calculations" : False})
        
        elif request.GET.get("test") in ["pair-t", "pair-z"]:
            return render(request, "partials/tz2_pairedform.html", {"calculations" : False})
        
        elif request.GET.get("test") == "ind-prop":
            return render(request, "partials/prop2form.html", {"calculations" : False})
        
        elif request.GET.get("test") == "mcnemar":
            return render(request, "partials/mcnemarform.html", {"calculations" : False})
        
        else:
            return render(request, "partials/tukeyform.html", {"calculations" : False})
    
    if request.method == "POST":

        template = "two-sample.html"

        test = request.POST.get("test")
        

        if test in ["ind-t", "pair-t", "ind-z", "pair-z"]:

            alternative = request.POST.get("alternative")
            equal_var = request.POST.get("equal_var")

            try:
                value = float(request.POST.get("value"))
                alpha = float(request.POST.get("alpha"))
            
            except:
                messages.add_message(request, messages.WARNING, "Value or alpha aren't numeric")
                return render(request, "two-sample.html", context={"calculations" : False})

            file = request.FILES.get("data_file")
            
            try:
                df = pd.read_csv(file)

            except:
                messages.add_message(request, messages.WARNING, "Couldn't Open File")
                return render(request, "two-sample.html", context={"calculations" : False})

            if test == "ind-t":

                try:
                    context = calc_ttest2(df, value, alternative, alpha, equal_var, False)
                    template = "partials/ttest_2.html"
                except:
                    messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                    context = {"calculations" : False}
        
            elif test == "pair-t":
                
                try:
                    context = calc_ttest2(df, value, alternative, alpha, equal_var, True)
                    template = "partials/ttest_2.html"
                except:
                    messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                    context = {"calculations" : False}
        
            elif test == "ind-z":

                try:
                    context = calc_ztest2(df, value, alternative, alpha, equal_var, False)
                    template = "partials/ztest_2.html"
                except:
                    messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                    context = {"calculations" : False}

            elif test == "pair-z":

                try:
                    context = calc_ztest2(df, value, alternative, alpha, equal_var, True)
                    template = "partials/ztest_2.html"
                except:
                    messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                    context = {"calculations" : False}

        elif test == "ind-prop":

            alternative = request.POST.get("alternative")
            method = request.POST.get("method")

            try:
                value = float(request.POST.get("value"))
                alpha = float(request.POST.get("alpha"))
            
            except:
                messages.add_message(request, messages.WARNING, "Value or alpha aren't numeric")
                return render(request, "two-sample.html", context={"calculations" : False})

            try:
                successes1 = int(request.POST.get("successes1"))
                trials1 = int(request.POST.get("trials1"))
                successes2 = int(request.POST.get("successes2"))
                trials2 = int(request.POST.get("trials2"))
            except:
                messages.add_message(request, messages.WARNING, "Successes or Trials aren't integers")
                context = {"calculations" : False}

            try:
                context = calc_prop2(successes1, trials1, successes2, trials2, value, alternative, alpha, method)
                template = "partials/prop2.html"
            except:
                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}

        elif test == "mcnemar":

            try:
                alpha = float(request.POST.get("alpha"))
            except:
                messages.add_message(request, messages.WARNING, "Alpha not numeric")
                return render(request, "two-sample.html", context={"calculations" : False})
            
            try:
                pos_pos = int(request.POST.get("pos-pos"))
                pos_neg = int(request.POST.get("pos-neg"))
                neg_pos = int(request.POST.get("neg-pos"))
                neg_neg = int(request.POST.get("neg-neg"))
            except:
                messages.add_message(request, messages.WARNING, "Table doesn't have all integers")
                context = {"calculations" : False}

            try:
                context = calc_mcnemar(pos_pos, pos_neg, neg_pos, neg_neg, alpha)
                template = "partials/mcnemar.html"
            except:
                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}

        elif test == "tukey":

            try:
                alpha = float(request.POST.get("alpha"))
            
            except:
                messages.add_message(request, messages.WARNING, "Alpha not numeric")
                return render(request, "two-sample.html", context={"calculations" : False})

            file = request.FILES.get("data_file")
            
            try:
                df = pd.read_csv(file)

            except:
                messages.add_message(request, messages.WARNING, "Couldn't Open File")
                return render(request, "two-sample.html", context={"calculations" : False})
        
            try:
                context = calc_tukey(df, alpha)
                template = "partials/tukey.html"
            except:
                messages.add_message(request, messages.WARNING, "Couldn't Calculate")
                context = {"calculations" : False}
            

        return render(request, template, context=context)


    return render(request, "two-sample.html", {"calculations" : False})
