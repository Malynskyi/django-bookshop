from django.shortcuts import render
from demo_app.models import DemoModel
from books.awkward_file import BookOrDemoView


def all_demo(request):
    return render(request, 'all_records.html', {
        'demo_models': DemoModel.objects.filter(is_visible=True)
    })


class AllDemo(BookOrDemoView):
    model = DemoModel


