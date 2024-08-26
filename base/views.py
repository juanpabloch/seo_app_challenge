from django.shortcuts import render, redirect

from base.forms import UrlSelectionForm
from base.services import get_url_data, save_urls_comparison
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UrlSelectionForm(request.POST)
        if form.is_valid():
            data = {}
            data["url_1"] = get_url_data(form.cleaned_data["url_1"], form.cleaned_data["strategy"])
            data["url_2"] = get_url_data(form.cleaned_data["url_2"], form.cleaned_data["strategy"])

            if data["url_1"] and data["url_2"]:
                request.session['form_data'] = data
                return redirect('results')
            else:
                # message error
                pass
        else:
            return render(request, 'home.html', {"form": form})
    
    form = UrlSelectionForm()
    context = {
        "form": form
    }
    return render(request, 'home.html', context)


def results(request):
    print("VISTA")
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('home')

    save_urls_comparison(form_data)

    request.session["form_data"] = None
    context = {
        "data": form_data
    }
    return render(request, 'results.html', context)
