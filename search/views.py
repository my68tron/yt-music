from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, FileResponse
from search.models import Search, Song
from search import forms
from search.yt_scrape import yt_scrape_bs
from django.conf import settings
import os
import json

# Store songs to database
def storeSongs(search_input):
    scrape_result = yt_scrape_bs(search_input)

    song_ids = []
    for link in scrape_result['scraped_links']:
        try:
            song = Song.objects.get(url=link['url'].replace('/watch?v=', ''))
        except Song.DoesNotExist:
            song = Song.objects.create(
                name=link['name'],
                duration=link['duration'],
                url=link['url'].replace('/watch?v=', ''),
                img_url=link['img_url'],
                channel_name=link['channel_name'],
                channel_url=link['channel_url'],
                uploaded=link['uploaded'],
                views=link['views']
            )
        finally:
            song_ids.append(song.id)
    return (scrape_result['scraped_links'], scrape_result['search_input'], song_ids)

# Display search results or display search page
def index(request):
    search_list = Search.objects.all()[:10]
    context = {'search_list': search_list}

    if request.method == 'GET' and 'search' in request.GET:
        context['search_input'] = search_input = request.GET['search']
        
        try:
            search = Search.objects.get(title=search_input)
            if 'f' in request.GET:
                (context['search_results'], context['search_input'], song_ids) = storeSongs(search_input)
                search.songs = ','.join(map(str, song_ids))
                search.save()
            else:
                song_ids = list(map(int, search.songs.split(',')))
                search_results = []
                for song_id in song_ids:
                    search_results.append(Song.objects.get(id=song_id))
                context['search_results'] = search_results
        except Search.DoesNotExist:
            (context['search_results'], context['search_input'], song_ids) = storeSongs(search_input)
            Search(title=context['search_input'], songs=','.join(map(str, song_ids))).save()

        return render(request, 'search/results.html', context=context)

    return render(request, 'search/index.html', context=context)

# Contact Us Page
def contact(request):
    search_list = Search.objects.all()[:10]
    context = {'search_list': search_list}

    if request.method == 'POST':
        if form.is_valid():
            print("Validation Success!")
            print("Name = " , form.cleaned_data['name'])
            print("email = " , form.cleaned_data['email'])
            print("textarea = " , form.cleaned_data['textarea'])

            return render(request, 'search/form_example.html', context=context)

    return render(request, 'search/under_construction.html', context=context)