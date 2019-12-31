import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yt_website.settings')

import django
django.setup()

# Fake Pop Scripts / Fake Population Scripts
import random
from search.models import Song, Search
from faker import Faker

faker = Faker()

def populate(N=5):
    for entry in range(N):
        fake_title = faker.name()
        fake_url = faker.url()

        search = Search.objects.get_or_create(search_title=fake_title)[0]
        search.save()

if __name__ == '__main__':
    print("Starting Populating Script")
    populate(10)
    print("Populating Complete")