from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse, HttpResponseBadRequest
from download.yt_download import yt_download, yt_info
from search.models import Search, Song
from download.models import DownloadedSong
from django.conf import settings
import os
import json

# Download mp3 from url
def download_url(request, id):
    try:
        song = Song.objects.get(pk=int(id))
        duration = song.duration
        if ':' in duration:
            duration = list(map(int, duration.split(':')))[::-1]
            if len(duration) > 2:
                duration = duration[0] + (60 * duration[1]) + (3600 * duration[2])
            else:
                duration = duration[0] + (60 * duration[1])
        try:
            downloadedSong = DownloadedSong.objects.get(pk=int(id))
            if downloadedSong.path == '':
                raise DownloadedSong.DoesNotExist()
        except DownloadedSong.DoesNotExist:
            downloadedSong, created = DownloadedSong.objects.get_or_create(pk=int(id), song=song)
            yt_download(song.url, int(duration))
            file_name = song.name + '.mp3'
            # For Linux Server
            # for c in "()[],&":
            #     file_name = file_name.replace(c, '')
            # file_name = '_'.join(file_name.split())
            # file_name = file_name.translate(None, '()')
            downloadedSong.path = file_name
            downloadedSong.save()

        return HttpResponse("Success!")
    except Song.DoesNotExist:
        flash_message = {
            'message': 'Invalid Song Id',
            'css_type': 'danger'
        }
        response = HttpResponse(json.dumps({'error-message': flash_message}), 
            content_type='application/json')
        response.status_code = 400
        return response
    return HttpResponseBadRequest('Bad Request')

# Download a media file using POST request
def download_file(request):
    downloaded_songs = DownloadedSong.objects.all().order_by('-updated')
    search_list = Search.objects.all()[:10]
    context = {'search_list': search_list, 'downloaded_songs': downloaded_songs}

    if request.method == 'GET' and 'id' in request.GET:
        downloaded_song = DownloadedSong.objects.get(pk=int(request.GET['id']))
        file_name = downloaded_song.path
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        if os.path.exists(file_path):
            downloaded_song.download_count = downloaded_song.download_count + 1
            downloaded_song.save()
            response = FileResponse(open(file_path, 'rb'), as_attachment=True)
            return response
        else:
            flash_message = {
                'message': 'Song Does Not Exist!',
                'css_type': 'danger'
            }
            context['flash_message'] = flash_message

    return render(request, 'download/file.html', context=context)
# Download Page to enter url
def download_page(request):
    search_list = Search.objects.all()[:10]
    context = {'search_list': search_list}

    if request.method == 'GET' and 'download' in request.GET:
        url = request.GET['download']
        context['download_url'] = url
        try:
            song_info = yt_info(url)
            if song_info:
                try:
                    song = Song.objects.get(url=song_info['id'])
                except Song.DoesNotExist:
                    song = Song.objects.create(
                        name=song_info['title'],
                        duration=song_info['duration'],
                        url=song_info['id'],
                        img_url=song_info['thumbnail'],
                        channel_name=song_info['uploader'],
                        channel_url='/channel/' + song_info['channel_id'],
                        uploaded=song_info['upload_date'],
                        views=song_info['view_count']
                    )

                return redirect(reverse('download:download_url', kwargs={'id': song.id}), permanent=False)
            else:
                raise Exception('Incorrect URL')
        except Exception as e:
            flash_message = {
                'message': str(e),
                'css_type': 'danger'
            }
            response = HttpResponse(json.dumps({'error-message': flash_message}), 
                content_type='application/json')
            response.status_code = 400
            return response

    return render(request, 'download/index.html', context=context)
