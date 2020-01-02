import urllib.parse

##* Used for Selenium Scraping
# from selenium import webdriver
# import pandas as pd

from bs4 import BeautifulSoup
import requests

##* Used for Selenium Scraping
# Default Selenium driver
# driver = webdriver.Chrome()

BASE_URL = 'https://youtube.com/'
SEARCH_RESULT_PAGE = 'results?search_query='

def yt_scrape_bs(search_text ='lollipop onderkoffer'):
    query = urllib.parse.quote_plus(search_text, safe='')

    r = requests.get(BASE_URL + SEARCH_RESULT_PAGE + query)
    soup = BeautifulSoup(r.content, 'html5lib')

    import os
    from django.conf import settings
    with open(os.path.join(settings.MEDIA_ROOT, 'url.txt'), 'w', encoding='utf-8') as f_out:
        f_out.write(soup.prettify())

    video_tiles = soup.findAll('div', attrs={'class':'yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix'})
    scraped_links = []
    tile_id = 1
    for video_tile in video_tiles[:10]:
        scraped_content = {}
        scraped_content['id'] = tile_id
        tile_id += 1

        video_thumbnail = video_tile.find('span', attrs={'class': 'yt-thumb-simple'})
        
        img = video_thumbnail.find('img')
        duration = video_thumbnail.find('span', attrs={'class': 'video-time'})
        scraped_content['img_url'] = img['src'] if 'https://i.ytimg.com' in img['src'] else img['data-thumb']
        scraped_content['duration'] = duration.get_text()

        content = video_tile.find('div', attrs={'class': 'yt-lockup-content'})

        title = content.find('h3', attrs={'class': 'yt-lockup-title'})
        title = title.find('a')
        scraped_content['url'] = title['href']
        scraped_content['name'] = title.get_text()

        channel_info = content.find('div', attrs={'class': 'yt-lockup-byline'})
        channel_info = channel_info.find('a', attrs={'class': 'yt-uix-sessionlink spf-link'})
        scraped_content['channel_url'] = channel_info['href']
        scraped_content['channel_name'] = channel_info.get_text()

        meta = content.find('div', attrs={'class': 'yt-lockup-meta'})
        meta_info = content.find('ul', attrs={'class': 'yt-lockup-meta-info'})
        meta_info = meta_info.find_all('li')
        scraped_content['uploaded'] = meta_info[0].get_text()
        scraped_content['views'] = meta_info[1].get_text() if len(meta_info) > 1 else '-'
      
        scraped_links.append(scraped_content)

    search_input = search_text
    # check if spelling is corrected by Youtube
    spell_check = soup.find('a', attrs={'class': 'spell-correction-corrected-query'})
    if spell_check:
        spell_check = spell_check['href'].replace('/results?search_query=', '')
        spell_check = urllib.parse.unquote(spell_check)
        search_input = ' '.join(spell_check.split('+'))

    result = {'scraped_links': scraped_links, 'search_input': search_input}

    return result

##* Used for Selenium Scraping
#* Scraping using selenium is easy to do and for data collecting for AI projects
def yt_scrape_sel(search_text = 'lollipop onderkoffer'):
    search_text = urllib.parse.quote_plus(search_text, safe='')
    driver.get(BASE_URL + SEARCH_RESULT_PAGE + search_text)

    data = driver.find_elements_by_xpath('//*[@id="dismissable"]')

    scraped_links = []
    count = 1

    for i in data:
        meta = i.find_elements_by_id('meta')
        if len(meta) > 1:
            continue
        meta = meta[0]
        metadata = i.find_element_by_id('metadata')

        scraped_content = {}

        data = meta.find_element_by_id('video-title')
        scraped_content['title'] = data.get_attribute('title')
        scraped_content['aria-label'] = data.get_attribute('aria-label')
        scraped_content['url'] = data.get_attribute('href')

        channel_info = metadata.find_element_by_id('text')
        channel_info = channel_info.find_element_by_tag_name('a')
        scraped_content['channel-name'] = channel_info.text
        scraped_content['channel-link'] = channel_info.get_attribute('href')

        video_views = metadata.find_element_by_id('metadata-line')
        video_views = video_views.find_elements_by_tag_name('span')
        scraped_content['view_count'] = video_views[0].text
        scraped_content['video_uploaded'] = video_views[1].text

        #TODO Extract thumbnail as id for image and duration
        
        # print(count , " | ", scraped_content['title'], " | ", channel_info.text, " | ", scraped_content['view_count'], " | ", scraped_content['video_uploaded'])
        count += 1
        scraped_links.append(scraped_content)

    print(len(scraped_links))
    df = pd.DataFrame(columns = ['link', 'title', 'description', 'category'])

    return scraped_links

if __name__ == "__main__":
    ##* Used for Selenium Scraping
    # print(yt_scrape_sel('dimitri vegas & like mike tomorrowland 2019'))
    print(yt_scrape_bs('choppa dunks'))
    pass