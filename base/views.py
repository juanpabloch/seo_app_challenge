from django.shortcuts import render, redirect
import requests

from base.forms import UrlSelectionForm
from core import settings
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UrlSelectionForm(request.POST)
        if form.is_valid():
            print("PASO")
            request.session['form_data'] = form.cleaned_data
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

    base_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?category=performance'
    page = f'&url={form_data["url_1"]}'
    strategy = f'&strategy={form_data["strategy"]}'
    
    if settings.API_KEY:
        page += f'&key={settings.API_KEY}'

    print(base_url + page + strategy)
    # https://www.googleapis.com/pagespeedonline/v5/runPagespeed?category=performance&url=https://www.nelanegri.com/&key= AIzaSyCIIh9QB4M9pN5mtra_VjudRGS8cgDhWQ0 &strategy=desktop
    # DATA:  {'url_1': 'https://www.nelanegri.com/', 'url_2': 'https://juanpabloch.github.io/porfolio_jp/', 'strategy': 'desktop'}
    response = requests.get(base_url + page + strategy)
    result = response.json()
    data = {
        "speed": result['lighthouseResult']['audits']['speed-index'],
        "interactive": result['lighthouseResult']['audits']['interactive'],
    }

    request.session.flush()

    print("DATA: ", data)
    context = {
        "data": data
    }
    return render(request, 'results.html', context)
