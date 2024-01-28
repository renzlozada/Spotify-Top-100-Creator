import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


class SpotifyManager:
    def __init__(self):
        self.playlist_id = None
        self.sp = None
        self.id_list = []
        self.user_id = os.environ["USER_ID"]

    def authenticate(self):
        """
        Authenticate with the actual Spotify API
        :param:
        :return:
        """
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.environ["CLIENT_ID"],
                client_secret=os.environ["CLIENT_SECRET"],
                redirect_uri="http://example.com",
                scope="playlist-modify-private user-read-private user-library-modify",
            )
        )

    def find_track_id(self, titles, year):
        for idx in range(len(titles)):
            try:
                track_id = self.sp.search(
                    q=f"track:{titles[idx]}+year:{year}", type="track", market="US"
                )
                track_id = track_id["tracks"]["items"][0]["uri"]
                self.id_list.append(track_id)
            except IndexError as err:
                print(f"No track ID for {titles[idx]}")

    def create_playlist(self, date_format):
        self.playlist_id = self.sp.user_playlist_create(
            user=self.user_id,
            name=f"{date_format} Billboard Top 100",
            public=False,
            description="Python Made playlist in UDemy\n" "Created by RLozada",
        )
        self.playlist_id = self.playlist_id["id"]

    def add_items_to_playlist(self):
        self.sp.playlist_add_items(
            playlist_id=self.playlist_id, items=self.id_list, position=0
        )
        print(f"Playlist Created!")
