from youtube_dl import YoutubeDL
import os

class MyLogger(object):
    def debug(self, msg):
        print('debug : ', msg)

    def warning(self, msg):
        print('warning : ', msg)

    def error(self, msg):
        print('error : ', msg)
        raise Exception('ERROR!!!')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(BASE_DIR, 'media') +'/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
}

ydl = YoutubeDL(ydl_opts)

def yt_info(link:str):
    return True if ydl.extract_info(link, download=False) else False

def yt_download(link:str):
    page_info = ydl.extract_info(link, download=False)

    if int(page_info['duration']) >= 600:
        raise Exception("Videos more than 10 min long are not allowed to download")

    ydl.download([link])
    return page_info

if __name__ == "__main__":
    print(yt_download('YykjpeuMNEk'))
    pass