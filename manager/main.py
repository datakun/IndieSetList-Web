from flask import Flask, render_template, request, redirect, url_for, make_response

# import ssl

import datetime

import db_controller
from db_controller import Artist
from db_controller import Venue
from db_controller import Video
from db_controller import Event
from db_controller import Performance

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
        venues = [temp_str.strip() for temp_str in venues_cookie.split(',')]

    if artists_cookie is None:
        artists = db_controller.get_artist_list(is_object = False)
    else:
        artists = [temp_str.strip() for temp_str in artists_cookie.split(',')]
    
    # 공연장, 음악가 정보를 template에 전달하기 위한 준비
    resp = make_response(render_template('insert-perform.html', venue_list = venues, artist_list = artists))
    resp.set_cookie('venues', ','.join(venues))
    resp.set_cookie('artists', ','.join(artists))

    if request.method == 'POST':
        date = request.form['date']
        date = date.strip()
        venue = request.form['venue']
        venue = venue.strip()
        venue_object = db_controller.get_venue_by_name(venue).to_simple_dict()
        event_object = db_controller.get_event_by_date_venue_name(date, venue)

        if event_object is not None:
            artist = request.form['artist']
            artist = artist.strip()
            artist_object = db_controller.get_artist_by_name(artist).to_simple_dict()
            video_id = request.form['video-id']
            title = request.form['title']
            video = Video(video_id, title)

            perform = perform = Performance(u'', artist_object, date, event_object.id, venue_object, video.to_dict())
            print(perform)
            db_controller.insert_performance(perform)

    return resp

@app.route('/insert-artist', methods = ['GET', 'POST'])
def insert_artist():
    artists = []
    artists_cookie = request.cookies.get('artists')
    if artists_cookie is None:
        artists = db_controller.get_artist_list(is_object = False)
    else:
        artists = [temp_str.strip() for temp_str in artists_cookie.split(',')]
        
    resp = make_response(render_template('insert-artist.html'))

    # POST 로 실행 시, 음악가 삽입
    if request.method == 'POST':
        artist = request.form['artist']
        artist = artist.strip()

        db_controller.insert_artist(artist)

        artists.append(artist)
        
        resp.set_cookie('artists', ','.join(artists))

    return resp

@app.route('/insert-venue', methods = ['GET', 'POST'])
def insert_venue():
    venues = []
    venues_cookie = request.cookies.get('venues')
    if venues_cookie is None:
        venues = db_controller.get_venue_list(is_object = False)
    else:
        venues = [temp_str.strip() for temp_str in venues_cookie.split(',')]
        
    resp = make_response(render_template('insert-venue.html'))

    # POST 로 실행 시, 공연장 삽입
    if request.method == 'POST':
        venue = request.form['venue']
        venue = venue.strip()

        db_controller.insert_venue(venue)

        venues.append(venue)
        
        resp.set_cookie('venues', ','.join(venues))

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
        venues = [temp_str.strip() for temp_str in venues_cookie.split(',')]

    if artists_cookie is None:
        artists = db_controller.get_artist_list(is_object = False)
    else:
        artists = [temp_str.strip() for temp_str in artists_cookie.split(',')]
    
    # 공연장, 음악가 정보를 template에 전달하기 위한 준비
    resp = make_response(render_template('insert-event.html', venue_list = venues, artist_list = artists))
    resp.set_cookie('venues', ','.join(venues))
    resp.set_cookie('artists', ','.join(artists))

    # POST 로 실행 시, 공연 삽입
    if request.method == 'POST':
        date = request.form['date']
        date = date.strip()
        venue = request.form['venue']
        venue = venue.strip()
        venue_object = db_controller.get_venue_by_name(venue).to_simple_dict()
        artist_list_string = request.form['artist-list']
        artist_list_string = artist_list_string.strip()
        artist_list = []

        for artist in list(filter(None, [temp_str.strip() for temp_str in artist_list_string.split(',')])):
            artist_object = db_controller.get_artist_by_name(artist)
            artist_list.append(artist_object.to_simple_dict())

        event = Event(u'', date, venue_object, artist_list)

        db_controller.update_or_insert_event(event)

    return resp

if __name__ == '__main__':
    # openssl
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='secret')
    # app.run(host="0.0.0.0", port=4443, ssl_context=ssl_context)

    # static auto reload
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)
