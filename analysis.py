import pandas as pd
import spotipy
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=""))

def songdeets(id):
    track=sp.track(id, market='IN')
    imgurl=track['album']['images'][0]['url']
    songurl=track['preview_url']
    return imgurl,songurl

def artistdeets(id):
    track=sp.track(id)
    artistid=track["artists"][0]["id"]
    artist=sp.artist(artistid)
    imgurl=artist["images"][0]["url"]
    songurl=track["preview_url"]
    return imgurl,songurl

def classifytime(col):
    labels=['midnight','earlymorn','morning','afternoon','evening','night']
    bins = [0, 4*3600, 8*3600, 12*3600, 16*3600, 20*3600, 24*3600]
    col=col.apply(lambda t: t.hour * 3600 + t.minute * 60 + t.second)
    col = pd.cut(col, bins=bins, labels=labels, right=False)
    return col


class MusicData:

    def __init__(self,df,tz) -> None:
        df=df[["ts","ms_played","master_metadata_track_name","master_metadata_album_artist_name","spotify_track_uri"]]
#############################TODO fix timezone handling######################################       
        # df.loc[:,'date']=df['ts'].str[:10]
        # df.loc[:,'time']=df['ts'].str[11:-1]
        # df.loc[:,'time']=pd.to_datetime(df['time'], format='%H:%M:%S')
        # df.loc[:,'time']=df['time'] + timedelta(minutes=-int(tz))
        # df.loc[:,'time']=df['time'].dt.time
        df.loc[:,'timeclass']=classifytime(pd.to_datetime(df['ms_played']))

        self.df=df
        self.songid=None

    def topsinger(self):

        df2=self.df.groupby(["master_metadata_album_artist_name"])["ms_played"].sum().reset_index()
        df2=df2.sort_values(["ms_played"],ascending=False).reset_index()
        top=str(df2["master_metadata_album_artist_name"].iloc[0])
        df3=self.df.loc[self.df["master_metadata_album_artist_name"]==top]
        df3=df3.groupby(["master_metadata_track_name","master_metadata_album_artist_name"])["ms_played"].sum().reset_index()
        df3=df3.sort_values(["ms_played"],ascending=False).reset_index()
        song1=str(df3["master_metadata_track_name"].iloc[0])
        song1id=self.df.loc[(self.df['master_metadata_track_name'] == song1) & (self.df['master_metadata_album_artist_name'] == top), 'spotify_track_uri'].iloc[0]
        
        if df3.shape[0]==1:
            song=song1id
        elif song1id==self.songid:
            song2=str(df3["master_metadata_track_name"].iloc[1])
            song2id=self.df.loc[(self.df['master_metadata_track_name'] == song2) & (self.df['master_metadata_album_artist_name'] == top), 'spotify_track_uri'].iloc[0]
            song=song2id
        else:
            song=song1id
        song=song[-22:]
        imgurl,songurl=artistdeets(song)
        return {'artistname': top, 'imgurl': imgurl, 'songurl': songurl}

    def topsong(self):

        df2=self.df.groupby(["master_metadata_track_name","master_metadata_album_artist_name"])["ms_played"].sum().reset_index()
        df2=df2.sort_values(["ms_played"],ascending=False).reset_index()
        top=str(df2["master_metadata_track_name"].iloc[0])
        artist=str(df2["master_metadata_album_artist_name"].iloc[0])
        songid=self.df.loc[(self.df['master_metadata_track_name'] == top) & (self.df['master_metadata_album_artist_name'] == artist), 'spotify_track_uri'].iloc[0]
        self.songid=songid
        songid=songid[-22:]
        imgurl,songurl=songdeets(songid)
        return {'songname': top,'artist': artist, 'imgurl': imgurl, 'songurl': songurl}

    def totalhours(self):

        total=self.df["ms_played"].sum()
        total/=60000
        if total<300:
            return f"{total:.0f} minutes"
        total/=60
        if total<1200:
            return f"{total:.0f} hours"
        total/=24
        return f"{total:.0f} days"
    
    def timeofday(self):
        df2=self.df.groupby(['timeclass'])["ms_played"].sum().reset_index()
        df2=df2.sort_values(["ms_played"],ascending=False).reset_index()
        tod=str(df2["timeclass"].iloc[0])
        names={"midnight":"Midnight Listener","earlymorn":"Early Riser","morning":"Morning Sunshine","afternoon":"Afternoon Groover","evening":"Evening Viber","night":"Night Owl"}
        tod=names[tod]
        return tod
