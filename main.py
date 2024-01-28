import requests
from bs4 import BeautifulSoup
from spotify_manager import SpotifyManager

date_format = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)
year = date_format.split("-")[0]
URL = "https://www.billboard.com/charts/hot-100/"

id_list = []

bboard_response = requests.get(url=URL + date_format)
billboard = bboard_response.text

soup = BeautifulSoup(billboard, "html.parser")
song_div = soup.select(selector="li h3", class_="c-title")
titles = [
    f"{items.getText().strip()}\n"
    for counter, items in enumerate(song_div)
    if counter < 100
]

with open("Top_100.txt", "w") as file:
    file.writelines(titles)

spotipy_handler = SpotifyManager()  # Initialize
spotipy_handler.authenticate()  # Authenticate the Key
spotipy_handler.find_track_id(
    titles=titles, year=year
)  # find track IDs in the playlist
print(spotipy_handler.id_list)  # print the list of all track ids found
spotipy_handler.create_playlist(date_format)
spotipy_handler.add_items_to_playlist()
