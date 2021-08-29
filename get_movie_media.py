import requests
from bs4 import BeautifulSoup



def get_movie_poster (MOVIE_ID):
    """
      input: код артиста из базы, песня(возможно null)
      если песня не заданы ищем все саундтреки по исполнителю
      """
    url = f'https://www.imdb.com/title/{MOVIE_ID}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','Accept-Language': 'en-US,en;q=0.9'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text,'html.parser')
    print('now_films: ' + MOVIE_ID)
    poster_el = soup.find('div', {'class': 'title-overview'}).find('div', {'class': 'poster'})
    if poster_el:
        poster_src = soup.find('div', {'class': 'title-overview'}).find('div', {'class': 'poster'}).find('img').get('src')
        if len(poster_src)>0:
            return poster_src


def get_movie_img_trailer (MOVIE_URL, USER_AGENT):
    """
      input: код артиста из базы, песня(возможно null)
      если песня не заданы ищем все саундтреки по исполнителю
      """
    url = f'https://www.imdb.com{MOVIE_URL}/'
    headers = {'User-Agent': USER_AGENT,'Accept-Language': 'en-US,en;q=0.9'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text,'html.parser')
    # print('now_films: ' + MOVIE_URL)
    trailer_el = soup.find('div', {'class': 'ipc-poster'})
    # print ('dfdsfs:' + trailer_el)
    if trailer_el:
        trailer_src = soup.find('div', {'class': 'ipc-poster'}).find('div', {'class': 'ipc-media--poster'}).find('img').get('src')
        if len(trailer_src)>0:
            return trailer_src
