from django.urls import path
from search import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
]
