from flask import Flask, render_template, request, redirect, url_for, make_response

# import ssl

import datetime

import db_controller
from db_controller import Artist
from db_controller import Venue
from db_controller import Video
from db_controller import Event
from db_controller import Performance

# 데이터 삽입 후 result 값 해석
# 0: 기본 상태, 1: 실패, -1: 성공, -2: 이미 삽입 됨

app = Flask(__name__)

@app.route('/')
@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')

@app.route('/insert-perform', methods = ['GET', 'POST'])
def insert_perform():
    venues = []
    artists = []

    # 쿠키에서 공연장, 음악가 정보 가져오기
    venues_cookie = request.cookies.get('venues')
    artists_cookie = request.cookies.get('artists')

    # 쿠키에서 공연장, 음악가 정보 없으면 db에서 가져오기 
    if venues_cookie is None:
        venues = db_controller.get_venue_list(is_object = False)
    else:
        venues = [temp_str.strip() for temp_str in venues_cookie.split('\n')]

    if artists_cookie is None:
        artists = db_controller.get_artist_list(is_object = False)
    else:
        artists = [temp_str.strip() for temp_str in artists_cookie.split('\n')]

    # 연주 삽입 결과 변수
    result = 0

    if request.method == 'POST':
        # 공연 날짜
        date = request.form['date']
        date = date.strip()

        # 공연장
        venue = request.form['venue']
        venue = venue.strip()  
        venue_object = db_controller.get_venue_by_name(venue)
        if venue_object is not None:
            venue_object = venue_object.to_simple_dict()

            # 공연 정보
            event_object = db_controller.get_event_by_date_venue_name(date, venue)
            if event_object is not None:
                # 음악가
                artist = request.form['artist']
                artist = artist.strip()
                artist_object = db_controller.get_artist_by_name(artist)
                if artist_object is not None:
                    artist_object = artist_object.to_simple_dict()

                    # 유튜브 영상 정보
                    video_id = request.form['video-id']
                    title = request.form['title']
                    video = Video(video_id, title)

                    # 연주 삽입
                    perform = perform = Performance(u'', artist_object, date, event_object.id, venue_object, video.to_dict())
                    db_result = db_controller.insert_performance(perform)
                    if db_result is None:
                        # 이미 삽입 됨
                        result = -2
                    elif hasattr(db_result, 'update_time') is False:
                        # 삽입 실패
                        result = 1
                    else:
                        result = -1
                else:
                    # 삽입 실패, 음악가 없음
                    result = 1
            else:
                # 삽입 실패, 공연 정보 없음
                result = 1
        else:
            # 삽입 실패, 공연장 없음
            result = 1
    
    # 공연장, 음악가 정보를 template에 전달하기 위한 준비
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=1)
    resp = make_response(render_template('insert-perform.html', venue_list = venues, artist_list = artists, result = result))
    resp.set_cookie('venues', '\n'.join(venues), expires=expire_date)
    resp.set_cookie('artists', '\n'.join(artists), expires=expire_date)

    return resp

@app.route('/insert-artist', methods = ['GET', 'POST'])
def insert_artist():
    artists = []
    artists_cookie = request.cookies.get('artists')
    if artists_cookie is None:
        artists = db_controller.get_artist_list(is_object = False)
    else:
        artists = [temp_str.strip() for temp_str in artists_cookie.split('\n')]

    result = 0

    # POST 로 실행 시, 음악가 삽입
    if request.method == 'POST':
        artist = request.form['artist']
        artist = artist.strip()

        db_result = db_controller.insert_artist(artist)

        if db_result is None:
            # 이미 삽입 됨
            result = -2
        elif hasattr(db_result, 'update_time') is False:
            # 삽입 실패
            result = 1
        else:
            result = -1

        if result < 1:
            artists.append(artist)
        
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=1)
    resp = make_response(render_template('insert-artist.html', result = result))
    resp.set_cookie('artists', '\n'.join(artists), expires=expire_date)

    return resp

@app.route('/insert-venue', methods = ['GET', 'POST'])
def insert_venue():
    venues = []
    venues_cookie = request.cookies.get('venues')
    if venues_cookie is None:
        venues = db_controller.get_venue_list(is_object = False)
    else:
        venues = [temp_str.strip() for temp_str in venues_cookie.split('\n')]

    result = 0

    # POST 로 실행 시, 공연장 삽입
    if request.method == 'POST':
        venue = request.form['venue']
        venue = venue.strip()

        db_result = db_controller.insert_venue(venue)

        if db_result is None:
            # 이미 삽입 됨
            result = -2
        elif hasattr(db_result, 'update_time') is False:
            # 삽입 실패
            result = 1
        else:
            result = -1

        if result < 1:
            venues.append(venue)
        
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=1)
    resp = make_response(render_template('insert-venue.html', result = result))
    resp.set_cookie('venues', '\n'.join(venues), expires=expire_date)

    return resp

@app.route('/insert-event', methods = ['GET', 'POST'])
def insert_event():
    venues = []
    artists = []

    # 쿠키에서 공연장, 음악가 정보 가져오기
    venues_cookie = request.cookies.get('venues')
    artists_cookie = request.cookies.get('artists')

    # 쿠키에서 공연장, 음악가 정보 없으면 db에서 가져오기 
    if venues_cookie is None:
        venues = db_controller.get_venue_list(is_object = False)
    else:
        venues = [temp_str.strip() for temp_str in venues_cookie.split('\n')]

    if artists_cookie is None:
        artists = db_controller.get_artist_list(is_object = False)
    else:
        artists = [temp_str.strip() for temp_str in artists_cookie.split('\n')]

    result = 0

    # POST 로 실행 시, 공연 삽입
    if request.method == 'POST':
        # 공연 날짜
        date = request.form['date']
        date = date.strip()

        # 공연장
        venue = request.form['venue']
        venue = venue.strip()  
        venue_object = db_controller.get_venue_by_name(venue)
        if venue_object is not None:
            venue_object = venue_object.to_simple_dict()
        
            artist_list_string = request.form['artist-list']
            artist_list_string = artist_list_string.strip()
            artist_list = []

            for artist in list(filter(None, [temp_str.strip() for temp_str in artist_list_string.split('\n')])):
                artist_object = db_controller.get_artist_by_name(artist)
                artist_list.append(artist_object.to_simple_dict())

            event = Event(u'', date, venue_object, artist_list)

            db_result = db_controller.update_or_insert_event(event)

            if db_result is None or hasattr(db_result, 'update_time') is False:
                # 삽입 실패
                result = 1
            else:
                result = -1
        else:
            # 삽입 실패, 공연장 없음
            result = 1
    
    # 공연장, 음악가 정보를 template에 전달하기 위한 준비
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=1)
    resp = make_response(render_template('insert-event.html', venue_list = venues, artist_list = artists, result = result))
    resp.set_cookie('venues', '\n'.join(venues), expires=expire_date)
    resp.set_cookie('artists', '\n'.join(artists), expires=expire_date)

    return resp

if __name__ == '__main__':
    # openssl
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='secret')
    # app.run(host="0.0.0.0", port=4443, ssl_context=ssl_context)

    # static auto reload
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=False)
