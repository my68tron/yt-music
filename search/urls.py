from django.urls import path
from search import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('download/<url>', views.download_url, name='download'),
    path('download_file', views.download_file, name='download_file'),
    path('contact', views.contact, name='contact'),
]
