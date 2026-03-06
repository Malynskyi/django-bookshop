from django.urls import path
from demo_app.views import all_demo

urlpatterns = [
    path('', all_demo, name='all_demo'),
]