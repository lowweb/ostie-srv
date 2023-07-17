#import requests
# from lxml import html
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

# import json
# from get_movie_img import get_movie_poster


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    input_file.close()
    return text

def get_media_info (ARTIST_ID,SEARCH_SONG,USER_AGENT,ACCEPT_LANGUAGE):
    """
      input: код артиста из базы, песня(возможно null)
      если песня не заданы ищем все саундтреки по исполнителю
      """

    url = f'https://www.imdb.com/name/{ARTIST_ID}/'
    #headers = {'User-Agent': USER_AGENT,'Accept-Language': ACCEPT_LANGUAGE}
    #response = requests.get(url, headers = headers)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent={USER_AGENT}')
    options.add_experimental_option('prefs', {'intl.accept_languages': ACCEPT_LANGUAGE})
    driver = webdriver.Chrome(executeble_path="/home/devman/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver",options=options)
    # driver = webdriver.Chrome(options=options)

    driver.get(url)
    btnElement = driver.find_element(By.ID, "name-filmography-filter-soundtrack")
    driver.execute_script("arguments[0].click();", btnElement);
    # добавить клик на кнопку "больше"
    time.sleep(1)  # seconds
    soup = BeautifulSoup(driver.page_source,'html.parser')

    # print(ARTIST_ID)
    # print(SEARCH_SONG)
    m_results = []

    # тестовый парсинг по файлу потом убрать
    # text = read_file('data/sound.html')
    # soup = BeautifulSoup(text,'html.parser')

    soundtrack_block = soup.find('div', {'class': 'filmo-section-soundtrack'})
    if soundtrack_block:
        # print('yes')
        films_list = soup.find('div', {'class': 'filmo-section-soundtrack'}).find_next('ul', {
            'class': 'ipc-metadata-list'}).find_all('li', {'class': 'ipc-metadata-list-summary-item'})
        # m_posters =[]
        # проходимся по фильмам/сериалам/шоу
        for item in films_list:
            # постер
            if item.find('img', {'class': 'ipc-image'}):
                m_poster = item.find('img', {'class': 'ipc-image'}).get('src')
            else:
                m_poster = 'null'
            # ссылка на фильм
            m_href = item.find('a').get('href')
            # id фильма пока пусто
            m_id = m_href.split('/')[2]
            # название фильма
            m_name = item.find('a').get('aria-label')
            # print(m_name)
            # год может быть пустым
            m_year = item.find('div', {'class': 'ipc-metadata-list-summary-item__cc'}).find_next('span', {
                'class': 'ipc-metadata-list-summary-item__li'}).text.strip()
            m_year = m_year if m_year != '' else 'unknown'
            # print(m_year)
            # песни
            m_songs = []
            m_episodes = []
            songs_upper_case = []
            songs_blocks = item.find('div', {'class': 'ipc-metadata-list-summary-item__tc'}).find_all('span', {
                'class': 'ipc-metadata-list-summary-item__li'})
            # создаем массив всех песен в фильме
            for block in songs_blocks:
                block = block.text
                if ('performer:' in block):
                    # print(song)
                    songs = block.strip().split(',')
                    # print ('split =',manySongs)
                    for song in songs:
                        # находим левые и правые кавычки, все что без "" откидываем
                        lf_pos = song.find('"') + 1
                        rgh_pos = song[lf_pos:].find('"') + lf_pos
                        if lf_pos and rgh_pos:
                            song = song[lf_pos:rgh_pos].strip()
                            m_songs.append(song)
                            songs_upper_case.append(song.upper())
                            # print(m_songs)
            if (len(SEARCH_SONG) != 0 and SEARCH_SONG.upper() in songs_upper_case):
                m_results.append({'mId': m_id,
                                  'mLink': m_href,
                                  'mName': m_name,
                                  'mYear': m_year,
                                  'mPoster': m_poster,
                                  'mEpisodes': m_episodes})
            if (len(SEARCH_SONG) == 0):
                m_results.append({'mId': m_id,
                                  'mLink': m_href,
                                  'mName': m_name,
                                  'mYear': m_year,
                                  'mPoster': m_poster,
                                  'mEpisodes': m_episodes,
                                  'mSongs': m_songs})
            # print(m_name)
            # print(m_songs)
    # print(len(m_results))
    # print(m_results)
        # print('==================================================')

    return m_results
