from django.urls import path
from demo_app.views import all_demo, AllDemo



urlpatterns = [
    path('', all_demo, name='all_demo'),
    path('all_cbv/', AllDemo.as_view(), name='all_demo_cbv')
]