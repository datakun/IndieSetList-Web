from typing import List, Dict

import developer

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# db 삽입
cred = credentials.Certificate(developer.SERVICE_ACCOUNT_KEY_PATH)
#firebase_admin.initialize_app(cred)

#cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': developer.GOOGLE_PROJECT_ID,
})

db = firestore.client()

# Artist 객체
class Artist(object):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.created_at = firestore.SERVER_TIMESTAMP
        self.updated_at = firestore.SERVER_TIMESTAMP

    @staticmethod
    def from_dict(source):
        artist = Artist(source[u'id'], source[u'name'])
        artist.created_at = source[u'created_at']
        artist.updated_at = source[u'updated_at']

        return artist
        
    @staticmethod
    def from_simple_dict(source):
        artist = Artist(source[u'id'], source[u'name'])

        return artist

    def to_dict(self):
        dest = {
            u'id': self.id,
            u'name': self.name,
            u'created_at': self.created_at,
            u'updated_at': self.updated_at
        }

        return dest

    def to_simple_dict(self):
        dest = {
            u'id': self.id,
            u'name': self.name
        }

        return dest

    def __repr__(self):
        return(u'Artist(id={}, name={})'
            .format(self.id, self.name))

# Venue 객체   
class Venue(object):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.created_at = firestore.SERVER_TIMESTAMP
        self.updated_at = firestore.SERVER_TIMESTAMP

    @staticmethod
    def from_dict(source):
        venue = Venue(source[u'id'], source[u'name'])
        venue.created_at = source[u'created_at']
        venue.updated_at = source[u'updated_at']

        return venue
        
    @staticmethod
    def from_simple_dict(source):
        venue = Venue(source[u'id'], source[u'name'])

        return venue

    def to_dict(self):
        dest = {
            u'id': self.id,
            u'name': self.name,
            u'created_at': self.created_at,
            u'updated_at': self.updated_at
        }

        return dest

    def to_simple_dict(self):
        dest = {
            u'id': self.id,
            u'name': self.name
        }

        return dest

    def __repr__(self):
        return(u'Venue(id={}, name={})'
            .format(self.id, self.name))

# Video 객체
class Video(object):
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title

    @staticmethod
    def from_dict(source):
        video = Video(source[u'id'], source[u'title'])

        return video

    def to_dict(self):
        dest = {
            u'id': self.id,
            u'title': self.title
        }

        return dest

    def __repr__(self):
        return(u'Video(id={}, title={})'
            .format(self.id, self.title))

# Event 객체
class Event(object):
    def __init__(self, id: str, date: str, venue: Dict[str, str], artists: List[Dict[str, str]]):
        self.id = id
        self.date = date
        self.venue = venue
        self.artists = artists
        self.created_at = firestore.SERVER_TIMESTAMP
        self.updated_at = firestore.SERVER_TIMESTAMP

    @staticmethod
    def from_dict(source):
        event = Event(source[u'id'], source[u'date'], source[u'venue'], source[u'artists'])
        event.created_at = source[u'created_at']
        event.updated_at = source[u'updated_at']

        return event

    @staticmethod
    def from_simple_dict(source):
        event = Event(source[u'id'], source[u'date'], source[u'venue'], source[u'artists'])

        # if u'artists' in source:
        #     for item in source[u'artists']:
        #         artist = Artist(item[u'id'], item[u'name'])
        #         event.artists.append(artist)

        return event

    def to_dict(self):
        dest = {
            u'id': self.id,
            u'date': self.date,
            u'venue': self.venue,
            u'artists': self.artists,
            u'created_at': self.created_at,
            u'updated_at': self.updated_at
        }

        # if self.artists:
        #     for artist in self.artists:
        #         dest[u'artists'].append(artist)

        return dest

    def to_simple_dict(self):
        dest = {
            u'id': self.id,
            u'date': self.date,
            u'venue': self.venue,
            u'artists': self.artists
        }

        # if self.artists:
        #     for artist in self.artists:
        #         dest[u'artists'].append(artist)

        return dest

    def __repr__(self):
        return(u'Event(id={}, date={}, venue={}, artists={})'
            .format(self.id, self.date, self.venue, self.artists))
            
# Performance 객체
class Performance(object):
    def __init__(self, id: str, artist: Dict[str, str], date: str, event_id: str, venue: Dict[str, str], video: Dict[str, str]):
        self.id = id
        self.artist = artist
        self.date = date
        self.event_id = event_id
        self.venue = venue
        self.video = video
        self.created_at = firestore.SERVER_TIMESTAMP
        self.updated_at = firestore.SERVER_TIMESTAMP

    @staticmethod
    def from_dict(source):
        perform = Performance(source[u'id'], source[u'artist'], source[u'date'], source[u'event'], source[u'venue'], source[u'video'])
        perform.created_at = source[u'created_at']
        perform.updated_at = source[u'updated_at']

        return perform

    @staticmethod
    def from_simple_dict(source):
        perform = Performance(source[u'id'], source[u'artist'], source[u'date'], source[u'event'], source[u'venue'], source[u'video'])

        return perform

    def to_dict(self):
        dest = {
            u'id': self.id,
            u'artist': self.artist,
            u'date': self.date,
            u'event': self.event_id,
            u'venue': self.venue,
            u'video': self.video,
            u'created_at': self.created_at,
            u'updated_at': self.updated_at
        }

        return dest

    def to_simple_dict(self):
        dest = {
            u'id': self.id,
            u'artist': self.artist,
            u'date': self.date,
            u'event': self.event_id,
            u'venue': self.venue,
            u'video': self.video
        }

        return dest

    def __repr__(self):
        return(u'Performance(id={}, artist={}, date={}, event={}, venue={}, video={})'
            .format(self.id, self.artist, self.date, self.event_id, self.venue, self.video))

# 필드 추가
# def temp_1():
#     docs = db.collection(u'performance').stream()
#     for doc in docs:
#         db_ref = db.collection(u'performance').document(doc.id)
#         db_ref.set({
#             'created_at': firestore.SERVER_TIMESTAMP,
#             'updated_at': firestore.SERVER_TIMESTAMP
#         }, merge=True)

# 필드 삭제
# def temp_2():
#     docs = db.collection(u'performance').stream()
#     for doc in docs:
#         db_ref = db.collection(u'performance').document(doc.id)
#         db_ref.update({
#             u'artist.created_at': firestore.DELETE_FIELD,
#             u'artist.updated_at': firestore.DELETE_FIELD
#         })

def temp_3(artist, date, event_id, venue, video):
    perform = perform = Performance(u'', artist.to_simple_dict(), date, event_id, venue.to_simple_dict(), video.to_dict())
    insert_performance(perform)

# events 컬렉션
def get_event_by_id(event_id):
    db_ref = db.collection(u'events')
    doc = db_ref.document(event_id).get()
    if doc.to_dict() is not None:
        return Event.from_dict(doc.to_dict())

    return None

def get_event_list_by_date(event_date):
    db_ref = db.collection(u'events')
    docs = db_ref.where(u'date', u'==', event_date).stream()

    item_list = []
    for doc in docs:
        item = Event.from_dict(doc.to_dict())
        item_list.append(item)

    return item_list

def get_event_list_by_artist_name(artist_name):
    artist = get_artist_by_name(artist_name)

    db_ref = db.collection(u'events')
    docs = db_ref.where(u'artists', u'array_contains', artist.to_simple_dict()).stream()

    item_list = []
    for doc in docs:
        item = Event.from_dict(doc.to_dict())
        item_list.append(item)

    return item_list

def get_event_list_by_venue_name(venue_name):
    venue = get_venue_by_name(venue_name)

    db_ref = db.collection(u'events')
    docs = db_ref.where(u'venue', u'==', venue.to_simple_dict()).stream()

    item_list = []
    for doc in docs:
        item = Event.from_dict(doc.to_dict())
        item_list.append(item)

    return item_list

def get_event_by_date_venue_name(event_date, venue_name):
    venue = get_venue_by_name(venue_name)

    db_ref = db.collection(u'events')
    docs = db_ref.where(u'venue', u'==', venue.to_simple_dict()).where(u'date', u'==', str(event_date)).stream()
    for doc in docs:
        return Event.from_dict(doc.to_dict())

    return None

def insert_event(event):
    event_item = get_event_by_date_venue_name(event.date, event.venue[u'name'])

    if event_item is None:
        db_ref = db.collection(u'events').document()
        event.id = db_ref.id

        return db_ref.set(event.to_dict())

    return None

def update_event(event):
    item = get_event_by_id(event.id)

    if item is not None:
        db_ref = db.collection(u'events').document(event.id)
        event['updated_at'] = firestore.SERVER_TIMESTAMP

        return db_ref.update(event.to_dict())

    return None

def update_or_insert_event(event):
    event_item = get_event_by_date_venue_name(event.date, event.venue[u'name'])

    if event_item is None:
        db_ref = db.collection(u'events').document()
        event.id = db_ref.id

        return db_ref.set(event.to_dict())
    else:
        return update_event(event)

def delete_event(event):
    db_ref = db.collection(u'events')

    return db_ref.document(event.id).delete()

# artists 컬렉션
def get_artist_by_id(artist_id):
    db_ref = db.collection(u'artists')
    doc = db_ref.document(artist_id).get()
    if doc.to_dict() is not None:
        return Artist.from_dict(doc.to_dict())

    return None

def get_artist_by_name(artist_name):
    db_ref = db.collection(u'artists')
    docs = db_ref.where(u'name', u'==', artist_name).stream()

    for doc in docs:
        item = Artist.from_dict(doc.to_dict())
        
        return item

    return None

def get_artist_list(is_object = True):
    if is_object is True:
        return db.collection(u'artists').stream()
    else:
        artist_list = []
        docs = db.collection(u'artists').stream()

        for doc in docs:
            artist_list.append(doc.to_dict()[u'name'])

        return artist_list

def insert_artist(artist_name):
    artist = get_artist_by_name(artist_name)

    if artist is None:
        db_ref = db.collection(u'artists').document()
        artist = Artist(db_ref.id, artist_name)

        return db_ref.set(artist.to_dict())

    return None

def update_artist(artist):
    item = get_artist_by_id(artist.id)

    if item is not None:
        db_ref = db.collection(u'artists').document(artist.id)
        artist['updated_at'] = firestore.SERVER_TIMESTAMP

        return db_ref.update(artist.to_dict())

    return None

def delete_artist(artist):
    db_ref = db.collection(u'artists')

    return db_ref.document(artist.id).delete()

# venues 컬렉션
def get_venue_by_id(venue_id):
    db_ref = db.collection(u'venues')
    doc = db_ref.document(venue_id).get()
    if doc.to_dict() is not None:
        return Venue.from_dict(doc.to_dict())

    return None

def get_venue_by_name(venue_name):
    db_ref = db.collection(u'venues')
    docs = db_ref.where(u'name', u'==', venue_name).stream()

    for doc in docs:
        item = Venue.from_dict(doc.to_dict())
        
        return item

    return None

def get_venue_list(is_object = True):
    if is_object is True:
        return db.collection(u'venues').stream()
    else:
        venue_list = []
        docs = db.collection(u'venues').stream()

        for doc in docs:
            venue_list.append(doc.to_dict()[u'name'])

        return venue_list

def insert_venue(venue_name):
    venue = get_venue_by_name(venue_name)

    if venue is None:
        db_ref = db.collection(u'venues').document()
        venue = Venue(db_ref.id, venue_name)

        return db_ref.set(venue.to_dict())

    return None

def update_venue(venue):
    item = get_venue_by_id(venue.id)

    if item is not None:
        db_ref = db.collection(u'venues').document(venue.id)
        venue['updated_at'] = firestore.SERVER_TIMESTAMP

        return db_ref.update(venue.to_dict())

    return None

def delete_venue(venue):
    db_ref = db.collection(u'venues')

    return db_ref.document(venue.id).delete()

# performance 컬렉션
def get_performance_by_id(perform_id):
    db_ref = db.collection(u'performance')
    doc = db_ref.document(perform_id).get()
    if doc.to_dict() is not None:
        return Performance.from_dict(doc.to_dict())

    return None

def get_performance_by_video_id(video_id):
    db_ref = db.collection(u'performance')
    docs = db_ref.where(u'video.id', u'==', video_id).stream()
    for doc in docs:
        return Performance.from_dict(doc.to_dict())

    return None

def get_performance_list_by_artist_name(artist_name):
    artist = get_artist_by_name(artist_name)

    db_ref = db.collection(u'performance')
    docs = db_ref.where(u'artist', u'==', artist.to_simple_dict()).stream()

    item_list = []
    for doc in docs:
        item = Performance.from_dict(doc.to_dict())
        
        item_list.append(item)

    return item_list

def get_performance_list_by_venue_name(venue_name):
    venue = get_venue_by_name(venue_name)

    db_ref = db.collection(u'performance')
    docs = db_ref.where(u'venue', u'==', venue.to_simple_dict()).stream()

    item_list = []
    for doc in docs:
        item = Performance.from_dict(doc.to_dict())
        
        item_list.append(item)

    return item_list

def get_performance_list_by_date(date):
    db_ref = db.collection(u'performance')
    docs = db_ref.where(u'date', u'==', date).stream()

    item_list = []
    for doc in docs:
        item = Performance.from_dict(doc.to_dict())
        
        item_list.append(item)

    return item_list

def insert_performance(perform):
    perform_item = get_performance_by_video_id(perform.video[u'id'])

    if perform_item is None:
        db_ref = db.collection(u'performance').document()
        perform.id = db_ref.id

        return db_ref.set(perform.to_dict())

    return None

def update_performance(perform):
    item = get_performance_by_id(perform.id)

    if item is not None:
        db_ref = db.collection(u'performance').document(perform.id)
        perform['updated_at'] = firestore.SERVER_TIMESTAMP

        return db_ref.update(perform.to_dict())

    return None

def delete_performance(perform):
    db_ref = db.collection(u'performance')

    return db_ref.document(perform.id).delete()