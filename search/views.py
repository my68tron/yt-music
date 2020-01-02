from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse
from search.models import Search
from search import forms
from search.yt_scrape import yt_scrape_bs
from search.yt_download import yt_download, yt_info
from django.conf import settings
import os
import json

# Display search results or display search page
def index(request):
    search_list = Search.objects.all()
    context = {'search_list': search_list}

    if request.method == 'POST':
        search_input = request.POST['search-input']
        context['search_input'] = search_input
        context['search_results'] = yt_scrape_bs(search_input)

        return render(request, 'search/results.html', context=context)

    return render(request, 'search/index.html', context=context)

# Download mp3 from url
def download_url(request, url):
    download_url = url if 'https://www.youtube.com/watch?v=' in url else 'https://www.youtube.com/watch?v=' + url
    context = {'download_url': download_url}
    try:
        page_info = yt_download(url)
        # print(json.dumps(page_info, indent=4, sort_keys=True))
    
        file_name = page_info['title'] + '.mp3'
        # For Linux Server
        # file_name = file_name.replace(' ', '')
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
    
    return render(request, 'search/download_page.html', context=context)

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

                return redirect(reverse('search:download', kwargs={'url': url}), permanent=True)
        except Exception as e:
            flash_message = {
                'message': str(e),
                'css_type': 'danger'
            }
            context['flash_message'] = flash_message

    return render(request, 'search/download_page.html', context=context)

# Contact Us Page
def contact(request):
    search_list = Search.objects.all()
    context = {'search_list': search_list}

    if request.method == 'POST':
        if form.is_valid():
            print("Validation Success!")
            print("Name = " , form.cleaned_data['name'])
            print("email = " , form.cleaned_data['email'])
            print("textarea = " , form.cleaned_data['textarea'])

            return render(request, 'search/form_example.html', context=context)

    return render(request, 'search/under_construction.html', context=context)