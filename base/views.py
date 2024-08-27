from django.shortcuts import render, redirect
from django.http import JsonResponse

from celery.result import AsyncResult

from base.forms import UrlSelectionForm
from base.services import save_urls_comparison
from base.task import get_url_data
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UrlSelectionForm(request.POST)
        if form.is_valid():
            url_1 = get_url_data.delay(form.cleaned_data["url_1"], form.cleaned_data["strategy"])
            url_2 = get_url_data.delay(form.cleaned_data["url_2"], form.cleaned_data["strategy"])

            if url_1 and url_2:
                request.session['form_data'] = {
                    "url_1": url_1.id,
                    "url_2": url_2.id,
                }
                return redirect('results')
            else:
                # message error
                pass
        else:
            return render(request, 'home.html', {"form": form})

    request.session['form_data'] = None
    form = UrlSelectionForm()
    context = {
        "form": form
    }
    return render(request, 'home.html', context)
    

def results(request):
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('home')
    
    result_1 = AsyncResult(form_data["url_1"])
    result_2 = AsyncResult(form_data["url_2"])

    if result_1.ready() and result_2.ready():
        if result_1.successful() and result_2.successful():
            data_1 = result_1.result
            data_2 = result_2.result
            save_urls_comparison({"url_1": data_1, "url_2": data_2, })
            return render(request, 'results.html', {"status": True, 'data_1': data_1, 'data_2': data_2})
        else:
            error_1 = result_1.result if not result_1.successful() else None
            error_2 = result_2.result if not result_2.successful() else None
            return render(request, 'results.html', {'error_1': error_1, 'error_2': error_2})

    context = {
        "status": False,
        "url_1_id": form_data["url_1"], 
        "url_2_id": form_data["url_2"]
    }
    return render(request, 'results.html', context)


def check_task_status(request):
    result_1 = AsyncResult(request.GET["task1"])
    result_2 = AsyncResult(request.GET["task2"])

    if result_1.ready() and result_2.ready():
        return JsonResponse({"status": "ready"})
    elif result_1.ready():
        return JsonResponse({"status": "almost", "task": "task1"})
    elif result_2.ready():
        return JsonResponse({"status": "almost", "task": "task2"})
    return JsonResponse({"status": "pending"})