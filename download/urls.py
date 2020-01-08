from django.urls import path
from download import views

app_name = 'download'
urlpatterns = [
    path('', views.download_page, name='download_page'),
    path('file', views.download_file, name='download_file'),
    path('url/<id>', views.download_url, name='download_url'),
]
