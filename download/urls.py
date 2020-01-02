from django.urls import path
from download import views

app_name = 'download'
urlpatterns = [
    path('', views.download_page, name='download_page'),
    path('<url>', views.download_url, name='download_url'),
    path('download_file', views.download_file, name='download_file'),
]
