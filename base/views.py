from django.shortcuts import render, redirect

from base.forms import UrlSelectionForm
from base.services import get_url_db, process_data, save_compare
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UrlSelectionForm(request.POST)
        if form.is_valid():
            data = {}
            data["url_1"] = get_url_db(form.cleaned_data["url_1"], form.cleaned_data["strategy"])
            data["url_2"] = get_url_db(form.cleaned_data["url_2"], form.cleaned_data["strategy"])

            request.session['form_data'] = data
            return redirect('results')
        else:
            return render(request, 'home.html', {"form": form})
    
    form = UrlSelectionForm()
    context = {
        "form": form
    }
    return render(request, 'home.html', context)


def results(request):
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('home')

    data = {}
    data["url_1"] = process_data(form_data["url_1"])
    data["url_2"] = process_data(form_data["url_2"])
    save_compare(data)
    request.session.flush()
    context = {
        "data": data
    }
    return render(request, 'results.html', context)
