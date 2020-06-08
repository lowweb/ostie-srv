from flask import Flask, request
from  get_imdb_nm_films import get_media_info
from flask_cors import CORS
import db_request
import get_movie_media
import datetime

app = Flask (__name__)
#CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.debug = true



@app.route('/api/info')
def main_view():
    return "Yep"


@app.route("/api/search")
def searsh_view():
    """
    'media': movie song
    'artist'
    'song
    """
    # пустой result
    data = {
        'resultsCount':'0',
        'results': []
    }


    artist = request.args.get('artist')
    song = request.args.get('song')
    media = request.args.get('media')
    artist_list = ''

    # если нет артиста и типа запроса то заворачиваем
    if not artist or not media:
        return data
    # пустая песня?значить ищем всего артиста
    if not song:
        song = ''
    if media == 'movie':
        # чекаем по базе артста
        artist_list = db_request.sql_request(f"Select fullname,nconst from artists where fullname='{artist}'")
        # artist_list = db_request.get_artist("Select fullname,nconst from artists where fullname=%s", artist)
        if len(artist_list)>0:
            for item in artist_list:
                data['resultsCount'] = len(artist_list)
                data['results'].append({'artist' : item['fullname'], 'artistData': get_media_info(item['nconst'], song)})
        else:
            return { 'resultsCount': 0,
                     'results': []}

        return  data

@app.route("/api/recent",methods=['GET','POST'])
def recent_view():
    if request.method == 'POST':
        req_data = request.get_json()
        film = f"{req_data['film']} ({req_data['year']})"
        artist = req_data['artist']
        song = req_data['song']
        movieUrl = req_data['link']

        #parsing img insert result
        imgUrl = get_movie_media.get_movie_img_trailer(movieUrl)
        if imgUrl is None:
            imgUrl='None'
        now = datetime.datetime.now()

        recentData = [film,artist,song,movieUrl,imgUrl,now.strftime("%Y-%m-%d %H:%M:%S")]
        db_request.insert_recent(recentData)
        # print(film)
        # print(song)
        return 'ok'
    if request.method == 'GET':
        recent = {
            'resultsCount': '0',
            'results': []
        }
        """return 10 records from recent"""
        recent_list = db_request.sql_request(f'Select film,artist,song,movieurl,imgurl from recent_search where imgurl <> "None" group by film,artist,song,movieurl,imgurl order by max(datetime) desc limit 10')
        if len(recent_list) > 0:
            for item in recent_list:
                recent['resultsCount'] = len(recent_list)
                recent['results'].append({'film': item['film'],
                               'imgurl': item['imgurl'],
                               'movieurl': item['movieurl'],
                               'artist': item['artist'],
                               'song': item['song']})
        else:
            return recent
        return recent



if __name__ == "__main__":
    app.run(host="127.0.0.1")