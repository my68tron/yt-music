from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse
from download.yt_download import yt_download, yt_info
from search.models import Search
from django.conf import settings
import os
import json

# Download mp3 from url
def download_url(request, url):
    download_url = url if 'https://www.youtube.com/watch?v=' in url else 'https://www.youtube.com/watch?v=' + url
    context = {'download_url': download_url}
    try:
        page_info = yt_info(download_url)
        yt_download(url, int(page_info['duration']))
        # print(json.dumps(page_info, indent=4, sort_keys=True))
    
        file_name = page_info['title'] + '.mp3'
        # For Linux Server
        # file_name = file_name.replace(' ', '_')
        # file_name = file_name.translate(None, '()')

        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            return response
        else:
            raise Exception('File Path not correct')
    except Exception as e:
        flash_message = {
            'message': str(e),
            'css_type': 'danger'
        }
        context['flash_message'] = flash_message
    
    return render(request, 'download/index.html', context=context)

# Download a media file using POST request
def download_file(request):
    if request.method == 'POST':
        title = request.POST['title']
        file_name = title + '.mp3'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            return response

# Download Page to enter url
def download_page(request):
    search_list = Search.objects.all()
    context = {'search_list': search_list}

    if request.method == 'POST':
        url = request.POST['download_url']
        context['download_url'] = url
        try:
            if yt_info(url):
                if 'https://www.youtube.com/watch?v=' in url:
                    url = url.replace('https://www.youtube.com/watch?v=', '')

                return redirect(reverse('download:download_url', kwargs={'url': url}), permanent=False)
            else:
                raise Exception('Incorrect URL')
        except Exception as e:
            flash_message = {
                'message': str(e),
                'css_type': 'danger'
            }
            context['flash_message'] = flash_message

    return render(request, 'download/index.html', context=context)
