# Youtube Music Downloading Website

You can search and download music files as mp3

**NOTE: Only Videos less than 10 min are allowed to download**

# How to setup

Setup your virtual environment and install packages required

`pip install -r requirements.txt`

Migrate models of each app

```python
python manage.py makemigrations search download
python manage.py migrate
```

Create super user for admin page

`python manage.py createsuperuser`

Run webserver

`python manage.py runserver`