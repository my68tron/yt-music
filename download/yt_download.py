from youtube_dl import YoutubeDL
import os

class YtLogger(object):
    def debug(self, msg):
        print('debug : ', msg)

    def warning(self, msg):
        print('warning : ', msg)

    def error(self, msg):
        print('error : ', msg)
        raise Exception('Incorrect URL')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(BASE_DIR, 'media') +'/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': YtLogger(),
}

ydl = YoutubeDL(ydl_opts)

def yt_info(link:str):
    page_info = ydl.extract_info(link, download=False)
    return page_info if page_info else False

def yt_download(link:str, duration:int):
    if int(duration) >= 600:
        raise Exception("Videos more than 10 min long are not allowed to download")

    ydl.download([link])
    return True

if __name__ == "__main__":
    print(yt_info('YykjpeuMNEk'))
    # print(yt_download('YykjpeuMNEk', 600))
    pass