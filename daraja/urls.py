from django.urls import path
from .views import InitiateSTKPush

app_name = 'daraja'

urlpatterns = [
    path('lipa-na-mpesa/', InitiateSTKPush.as_view(), name='lipa-na-mpesa'),
]