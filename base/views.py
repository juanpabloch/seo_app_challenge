from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from celery.result import AsyncResult

from base.models import UrlData
from base.forms import UrlSelectionForm
from base.services import save_urls_comparison
from base.task import get_url_data

STRATEGY = ["desktop", "mobile"]
ORDER = ["new", "old"]

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
                    "url1_text": form.cleaned_data["url_1"],
                    "url2_text": form.cleaned_data["url_2"],
                }
                return redirect('results')
            else:
                messages.error(request, "Error al analizar las URLs, por favor intente tarde")

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
            if result_1.result and result_2.result:
                save_urls_comparison({"url_1": result_1.result, "url_2": result_2.result, })
                return render(request, 'results.html', {"status": True, 'data_1': result_1.result, 'data_2': result_2.result})
        else:
            error_1 = result_1.result if not result_1.successful() else None
            error_2 = result_2.result if not result_2.successful() else None
            return render(request, 'results.html', {"status": False, 'error_1': error_1, 'error_2': error_2})

    context = {
        "status": False,
        "url_1_id": form_data["url_1"], 
        "url_2_id": form_data["url_2"],
        "url1_text": form_data["url1_text"],
        "url2_text": form_data["url2_text"],
    }
    return render(request, 'results.html', context)


def check_task_status(request):
    result_1 = AsyncResult(request.GET["task1"])
    result_2 = AsyncResult(request.GET["task2"])
    
    if result_1.result and result_2.result:
        return JsonResponse({"status": "ready"})

    elif result_1.ready():
        if not result_1.result:
            return JsonResponse({"status": "error", "task": "task1"})
        else:
            return JsonResponse({"status": "almost", "task": "task1"})

    elif result_2.ready():
        if not result_2.result:
            return JsonResponse({"status": "error", "task": "task2"})
        else:
            return JsonResponse({"status": "almost", "task": "task2"})

    return JsonResponse({"status": "pending"})


def history(request):
    filters = {
        "strategy": request.GET.get("strategy", None),
        "order": request.GET.get("order", None),
    }
    data = UrlData.objects.all()
    if filters["strategy"] and filters["strategy"] in STRATEGY:
        data = data.filter(strategy=filters["strategy"])

    if filters["order"] and filters["order"] in ORDER:
        data = data.order_by("-id") if filters["order"] == "new" else data.order_by("id")

    context = {
        "data": data,
        "filters": filters
    }
    return render(request, 'history.html', context)


def delete_history_item(request, item_id):
    try:
        item = UrlData.objects.get(id=item_id)
        item.delete()
        messages.success(request, "Item eliminado exitosamente")
    except Exception as err:
        messages.error(request, f"Error al eliminar el item")
        
    return redirect('history')