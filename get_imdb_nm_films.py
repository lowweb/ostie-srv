import requests
# from lxml import html
from bs4 import BeautifulSoup
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
    headers = {'User-Agent': USER_AGENT,'Accept-Language': ACCEPT_LANGUAGE}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text,'html.parser')

    # print(ARTIST_ID)
    # print(SEARCH_SONG)
    m_results = []

    # тестовый парсинг по файлу потом убрать
    # text = read_file('data/sound.html')
    # soup = BeautifulSoup(text,'html.parser')
    soundtrack_block = soup.find('div', {'id': 'filmo-head-soundtrack'})
    if  soundtrack_block:
        films_list = soup.find('div', {'id': 'filmo-head-soundtrack'}).find_next('div', {'class': 'filmo-category-section'}).find_all('div', {'class': 'filmo-row'})
        for item in films_list:
            # id фильма
            m_id = item.get('id')[11:]
            m_episodes = []
            # ссылка на фильм
            m_href = item.find('a').get('href')
            m_name = item.find('a').text
            # print(m_name)
            # может быть пустым
            m_year = item.find('span', {'class': 'year_column'}).text.strip()
            m_year = m_year if m_year != '' else 'unknown'
            m_songs = []
            episodes = item.find_all('div', {'class': 'filmo-episodes'})
            # если это сериал или передача
            if episodes:
                # print('episode')
                # сколько эпизодов в принципе не надо тк не все эпизоды будут в выдаче а там кол-во
                # print(item.contents[4].strip())
                for episode in episodes:
                    # m_episodes.append({'epName': episode.find('a').text,
                    #                     'epLink': episode.find('a').get('href')})
                    # получаем песню эпизода
                    songs = episode.contents[2].strip().split(',')
                    # создаем массив всех песен в фильме
                    for song in songs:
                        # находим левые и правые кавычки, все что без "" откидываем
                        lf_pos = song.find('"') + 1
                        rgh_pos = song[lf_pos:].find('"') + lf_pos
                        if lf_pos and rgh_pos:
                            song = song[lf_pos:rgh_pos].strip()
                            m_songs.append(song)

                    # print(f'songs: {songs}')
                    # если ищем артист - песня
                    if len(SEARCH_SONG) != 0:
                        for song in songs:
                            # находим левые и правые кавычки, все что без "" откидываем
                            lf_pos = song.find('"') + 1
                            rgh_pos = song[lf_pos:].find('"') + lf_pos
                            if lf_pos and rgh_pos:
                                # print
                                song = song[lf_pos:rgh_pos].strip()

                                # print (len(song))
                                if SEARCH_SONG.upper() == song.upper():
                                    m_episodes.append({'epName': episode.find('a').text,
                                                       'epLink': episode.find('a').get('href')})
                                    # m_results['mEpisodes'] = m_episodes
                                    # m_results.append({'mId': m_id,
                                    #                   'mLink': m_href,
                                    #                  'mName': m_name,
                                    #                  'mYear': m_year,
                                    #                   'mEpisodes': m_episodes})
                    # добавляем все песни по исполнителю
                    else:
                        m_episodes.append({'epName': episode.find('a').text,
                                           'epLink': episode.find('a').get('href')})
                        # print(m_results)
                        # m_results['mEpisodes'] = m_episodes
                        # m_results.append({'mId': m_id,
                        #                   'mLink': m_href,
                        #                   'mName': m_name,
                        #                   'mYear': m_year,
                        #                   'mEpisodes': m_episodes})
                if m_episodes:
                    m_poster = ""
                    # убрали данные о songs чтоб не заполнять массив
                    if len(SEARCH_SONG) != 0:
                        m_results.append({'mId': m_id,
                                          'mLink': m_href,
                                          'mName': m_name,
                                          'mYear': m_year,
                                          'mPoster': m_poster,
                                          'mEpisodes': m_episodes})
                    else:
                        m_results.append({'mId': m_id,
                                          'mLink': m_href,
                                          'mName': m_name,
                                          'mYear': m_year,
                                          'mPoster': m_poster,
                                          'mEpisodes': m_episodes,
                                          'mSongs': m_songs})
            # вариант медиа без эпизодов
            else:
                m_episodes = []
                songs = item.contents[4].strip().split(',')
                # создаем массив всех песен в фильме
                for song in songs:
                    # находим левые и правые кавычки, все что без "" откидываем
                    lf_pos = song.find('"') + 1
                    rgh_pos = song[lf_pos:].find('"') + lf_pos
                    if lf_pos and rgh_pos:
                        song = song[lf_pos:rgh_pos].strip()
                        m_songs.append(song)
                # если ищем по песни иначе по всему артисту
                if len(SEARCH_SONG) != 0:
                    # print(f'songsOnly={songs}' )
                    for song in songs:
                        lf_pos = song.find('"') + 1
                        rgh_pos = song[lf_pos:].find('"') + lf_pos
                        song = song[lf_pos:rgh_pos].strip()
                        # print(len(song))
                        # если ищем по артисту и песне
                        if SEARCH_SONG.upper() == song.upper():
                            # print('Y')
                            m_poster = ""
                            m_results.append({'mId': m_id,
                                              'mLink': m_href,
                                              'mName': m_name,
                                              'mYear': m_year,
                                              'mPoster': m_poster,
                                              'mEpisodes': m_episodes})
                        # print('film')
                # если ищем по артисту  в целом
                else:
                    m_poster = ""
                    m_results.append({'mId': m_id,
                                      'mLink': m_href,
                                      'mName': m_name,
                                      'mYear': m_year,
                                      'mPoster': m_poster,
                                      'mEpisodes': m_episodes,
                                      'mSongs': m_songs})





        # print('==================================================')

    return m_results
