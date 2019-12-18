import datetime
import re
from difflib import SequenceMatcher

from apiclient.discovery import build
from apiclient.errors import HttpError

import db_controller
from db_controller import Artist
from db_controller import Venue
from db_controller import Video
from db_controller import Event
from db_controller import Performance

import developer

# 경험으로 similar_ratio를 계속 보정하도록 해야할 듯
place_similar_ratio = 0.15
artist_similar_ratio = 0.20

regex_list = [r'\d{6}\s', r'\d{8}', r'\d{2}-\d{2}-\d{2}',
              r'\d{2}\.\d{2}\.\d{2}', r'\d{2}\s\d{2}\s\d{2}',
              r'\d{4}-\d{2}-\d{2}', r'\d{4}\.\d{2}\.\d{2}',
              r'\d{4}\s\d{2}\s\d{2}']

date_format_list = [u'%y%m%d', u'%Y%m%d', u'%y-%m-%d',
                    u'%y.%m.%d', u'%y %m %d',
                    u'%Y-%m-%d', u'%Y.%m.%d',
                    u'%Y %m %d']


def get_event_date_from_string(src_string, event_info):
    event_date = None

    for i in range(8):
        match = re.search(regex_list[i], ' ' + src_string + ' ')
        if match is None:
            continue

        try:
            event_date = datetime.datetime.strptime(match.group().strip(), date_format_list[i]).date()
            if event_date == datetime.datetime.strptime(event_info.date, u'%Y-%m-%d').date():
                break
        except ValueError as e:
            print('Date value error occurred:', e)

    return event_date


def youtube_search_artist(query_term, event_info, artist_info):
    youtube = build(developer.YOUTUBE_API_SERVICE_NAME,
                    developer.YOUTUBE_API_VERSION,
                    developerKey=developer.YOUTUBE_DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=query_term,
        part='id,snippet',
        fields='items(id(kind,videoId),snippet(title,description))',
        type='video',
        maxResults=10
    ).execute()

    for search_result in search_response.get('items', []):
        event_venue = None
        is_found_artist = False

        if search_result[u'id'][u'kind'] == u'youtube#video':
            video_id = search_result[u'id'][u'videoId']
            video_title = search_result[u'snippet'][u'title']
            video_description = search_result[u'snippet'][u'description']

            # 제목과 내용에서 공연 날짜를 10가지 포맷을 이용하여 비교 후 가져옴
            event_date = get_event_date_from_string(video_title, event_info)
            if event_date is None:
                event_date = get_event_date_from_string(video_description, event_info)
            prob = SequenceMatcher(None, event_info.venue[u'name'], video_title).ratio()

            # 제목이나 내용에서 장소를 찾았다면 공연장 정보 가져옴
            if prob > place_similar_ratio:
                event_venue = event_info.venue[u'name']
            else:
                prob = SequenceMatcher(None, event_info.venue[u'name'], video_description).ratio()
                if prob > place_similar_ratio:
                    event_venue = event_info.venue[u'name']

            # 이벤트 정보의 장소와 날짜를 제목에서 찾았다면, 아티스트 이름을 목록에 넣기
            if event_venue is event_info.venue[u'name'] and event_date == datetime.datetime.strptime(event_info.date, u'%Y-%m-%d').date():
                is_found_artist = True

            # 공연장과 공연 날짜를 찾지 못한 경우
            if is_found_artist is False:
                # 제목에서 음악가를 찾음
                if artist_info.name in video_title:
                    is_found_artist = True
                else:
                    prob_2 = SequenceMatcher(None, artist_info.name, video_title).ratio()
                    if prob_2 > artist_similar_ratio:
                        is_found_artist = True

            # 영상 정보에서 아티스트를 찾지 못하면 데이터베이스에 삽입하지 않음
            if is_found_artist is False:
                return

            video_info = Video(video_id, video_title)

            perform = Performance(u'', artist_info.to_simple_dict(), event_info.date, event_info.id, event_info.venue, video_info.to_dict())
            print(db_controller.insert_performance(perform))


def youtube_search(artist_name):
    event_list = db_controller.get_event_list_by_artist_name(artist_name)

    for event in event_list:
        artist = None
        for item in event.artists:
            if item[u'name'] == artist_name:
                artist = Artist(item[u'id'], item[u'name'])

                break

        event_date = datetime.datetime.strptime(event.date, u'%Y-%m-%d').date()
        try:
            for i in range(8):
                search_term = u'intitle:"' + artist_name + u'" ' + event.venue[u'name'] + u' "' + \
                                event_date.strftime(date_format_list[i]) + u'"'
                # print('search term: ', search_term)
                youtube_search_artist(search_term, event, artist)
        except HttpError as e:
            print(u'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

            break
