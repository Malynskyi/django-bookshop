from django.shortcuts import render
from demo_app.models import DemoModel


def all_demo(request):
    return render(request, 'all_records.html', {
        'demo_models': DemoModel.objects.filter(is_visible=True)
    })

# Create your views here.
