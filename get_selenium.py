from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


#
# def read_file(filename):
#     with open(filename) as input_file:
#         text = input_file.read()
#     input_file.close()
#     return text

option = webdriver.ChromeOptions()
option.add_argument("--headless")
# option.add_argument("--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1")
option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
# webdriver.Chrome(options=option)
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# option.add_argument('--lang=en-EN,ru;q=0.8,en-US;q=0.5,en;q=0.3')
option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:109.0) Gecko/20100101 Firefox/115.0")
#
driver = webdriver.Chrome(executable_path="/var/www/ostie.org/.wdm/drivers/chromedriver/linux64/114.0.5735.90/chromedriver",options=option)

# driver = webdriver.Chrome()


url = 'https://www.imdb.com/name/nm1736962/'
# url = 'https://www.python.org/'
driver.get(url)

btnElement = driver.find_element(By.ID, "name-filmography-filter-soundtrack")
# btnElement.click()
driver.execute_script("arguments[0].click();", btnElement);
# print(inputElement)
# добавить клик на кнопку "больше"
time.sleep(2)  # seconds

# # тестовый парсинг по файлу потом убрать
# text = read_file('data/civil.html')
# soup = BeautifulSoup(text,'html.parser')

#отдаем всю страницу Bsoap
soup = BeautifulSoup(driver.page_source, 'html.parser')
# SEARCH_SONG = 'Dust to Dust'
SEARCH_SONG = ''
m_results = []

soundtrack_block = soup.find('div', {'class': 'filmo-section-soundtrack'})
if  soundtrack_block:
    # print('yes')
    films_list = soup.find('div', {'class': 'filmo-section-soundtrack'}).find_next('ul', {'class': 'ipc-metadata-list'}).find_all('li', {'class': 'ipc-metadata-list-summary-item'})
    # m_posters =[]
    #проходимся по фильмам/сериалам/шоу
    for item in films_list:
        #постер
        if item.find('img',{'class': 'ipc-image'}):
            m_poster = item.find('img',{'class': 'ipc-image'}).get('src')
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
        m_year = item.find('div', {'class': 'ipc-metadata-list-summary-item__cc'}).find_next('span',{'class': 'ipc-metadata-list-summary-item__li'}).text.strip()
        m_year = m_year if m_year != '' else 'unknown'
        # print(m_year)
        #песни
        m_songs = []
        m_episodes = []
        songs_upper_case = []
        songs_blocks = item.find('div',{'class': 'ipc-metadata-list-summary-item__tc'}).find_all('span',{'class' : 'ipc-metadata-list-summary-item__li'})
        # создаем массив всех песен в фильме
        for block in songs_blocks:
            block=block.text
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
print(len(m_results))
# print(m_results)


driver.close()