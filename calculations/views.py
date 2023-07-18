import pandas as pd
from scipy.stats import ttest_1samp

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

            col1 = df.iloc[:, 0]

            t_test = ttest_1samp(col1, value, alternative=alternative)

            t_stat = t_test[0]
            p_value = t_test[1]
            freedom = t_test.df


            interval = t_test.confidence_interval(1-alpha)

            low = interval[0]
            high = interval[1]

            context = {
                "calculations" : True,
                "t_stat" : round(t_stat, 4),
                "p_value" : round(p_value, 4),
                "freedom" : freedom,
                "confidence" : (1-alpha)*100,
                "low" : round(low, 4),
                "high" : round(high, 4),
                "alpha" : alpha
            }

            return render(request, "one-sample.html", context=context)



    return render(request, "one-sample.html", {"calculations" : False})

def two_sample(request):
    return render(request, "two-sample.html")
