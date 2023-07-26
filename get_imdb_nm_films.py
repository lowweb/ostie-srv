from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os


# def read_file(filename):
#     with open(filename) as input_file:
#         text = input_file.read()
#     input_file.close()
#     return text

def get_media_info (ARTIST_ID,SEARCH_SONG,USER_AGENT,ACCEPT_LANGUAGE):
    """
      input: код артиста из базы, песня(возможно null)
      если песня не заданы ищем все саундтреки по исполнителю
      """
    os.system("killall firefox")
    url = f'https://www.imdb.com/name/{ARTIST_ID}/'
    #headers = {'User-Agent': USER_AGENT,'Accept-Language': ACCEPT_LANGUAGE}
    #response = requests.get(url, headers = headers)
    options = Options()
    options.add_argument("-headless")
    options.add_argument('-no-sandbox')
    # options.profile = "/home/foxman"
    options.add_argument(f'user-agent={USER_AGENT}')
    options.set_preference('intl.accept_languages', ACCEPT_LANGUAGE)
    #driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver",options=options)
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    m_results = []
    try:
        btnElement = driver.find_element(By.ID, "name-filmography-filter-soundtrack")
        # if button @soundtrack do not press
        if 'filmography-selected-chip-filter' not in btnElement.get_attribute('class').split():
            driver.execute_script("arguments[0].click();", btnElement);
    except:
        return m_results

    # some case if we see @see_also
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')

    # print(ARTIST_ID)
    # print(SEARCH_SONG)


    # txt parcing
    # text = read_file('data/sound.html')
    # soup = BeautifulSoup(text,'html.parser')

    soundtrack_block = soup.find('div', {'class': 'filmo-section-soundtrack'})
    if soundtrack_block:
        soundtrack_blocks=soup.find('div', {'class': 'filmo-section-soundtrack'}).find_next('div',{'class': 'sc-526668ed-3'})
        soundtrack_accordion = soundtrack_blocks.find_all('div',{'class': 'ipc-accordion'})
        for item in soundtrack_accordion:
            item_title = item.find('span', {'class': 'ipc-accordion__item__title'}).find('li',{'class': 'ipc-inline-list__item'}).text.split()
            if ('Previous' in item_title):
                soundtrack_previous_lists = item
        films_list =  soundtrack_previous_lists.find('ul', {'class': 'ipc-metadata-list'}).find_all('li', {'class': 'ipc-metadata-list-summary-item'})
        # parsing all film in lists
        for item in films_list:
            if item.find('img', {'class': 'ipc-image'}):
                m_poster = item.find('img', {'class': 'ipc-image'}).get('src')
            else:
                m_poster = 'null'
            m_href = item.find('a').get('href')
            m_id = m_href.split('/')[2]
            # m_name = item.find('a').get('aria-label')
            m_name = item.find('div', {'class': 'ipc-metadata-list-summary-item__c'}).find_next('a', {'class': 'ipc-metadata-list-summary-item__t'}).text.strip()
            m_year = item.find('div', {'class': 'ipc-metadata-list-summary-item__cc'}).find_next('span', {
                'class': 'ipc-metadata-list-summary-item__li'}).text.strip()
            m_year = m_year if m_year != '' else 'unknown'
            m_songs = []
            m_episodes = []
            songs_in_uppercase = []
            songs_blocks = item.find('div', {'class': 'ipc-metadata-list-summary-item__tc'}).find_all('span', {
                'class': 'ipc-metadata-list-summary-item__li'})
            for block in songs_blocks:
                block = block.text
                if ('performer:' in block or 'writer:' in block):
                    type_of_song = block[0:block.find(':')].strip()
                    songs = block.strip().split(',')
                    for song in songs:
                        lf_pos = song.find('"') + 1
                        rgh_pos = song[lf_pos:].find('"') + lf_pos
                        if lf_pos and rgh_pos:
                            song = song[lf_pos:rgh_pos].strip()
                            if (len(song)>0):
                                m_songs.append(''.join([song,'(',type_of_song,')']))
                            songs_in_uppercase.append(song.upper())
            if (len(SEARCH_SONG) != 0 and SEARCH_SONG.upper() in songs_in_uppercase):
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
    driver.close()
    driver.quit()
    return m_results
