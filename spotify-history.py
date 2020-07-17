import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

Base = declarative_base()

# create table played_track (id serial, artist_name text, song_name text);
class Track(Base):
    __tablename__ = 'played_track'

    id = Column(BIGINT, primary_key=true)
    artist_name = Column(String)
    song_name = Column(String)

postgre_uri = os.environ.get('POSTGRE_URI')
engine = create_engine(postgre_uri)
scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username='tomborel'))

hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
after = int(datetime.datetime.timestamp(hour_ago)) * 1000
results = sp.current_user_recently_played(after=after)
Session = sessionmaker(bind=engine)
session = Session()

for idx, item in enumerate(results['items']):
    track = item['track']
    played_at = item['played_at']
    formatted = datetime.datetime.strptime(played_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    print(idx, track['artists'][0]['name'], " – ", track['name'])
    played_track = Track(artist_name=track['artists'][0]['name'], song_name=track['name'])
    session.add(played_track)
    session.commit()
    print('Success!')
