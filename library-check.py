import requests
import io
import sys
from xml.dom import minidom


token = ''
torbox_key = ''

plex_ip = ''
torbox_api_ip = ''
torbox_port = 4004

res = requests.get(f"http://{plex_ip}:32400/library/sections/1/all?X-Plex-Token={token}")
file = io.StringIO(res.text)
xml = minidom.parse(file)
plex_movies = xml.getElementsByTagName('Video')

res = requests.get(f"http://{plex_ip}:32400/library/sections/2/all?X-Plex-Token={token}")
file = io.StringIO(res.text)
xml = minidom.parse(file)
plex_shows = xml.getElementsByTagName('Directory')

"""
Function to interface with the Yify API and return movie statistics. 
First argument, endpoint: is the string name of the API endpoint you want to access, such as "list_movies".
    - Only the name is needed, not the extension; .json is assumed and concatenated to the end
Further arguments are given as key-pair values associated with the desired endpoint parameters, such as limit=10.

See Yify API documentation at https://yts.torrentbay.to/api for endpoints and parameters.
"""
def yify(endpoint, **kwargs):
    url = f"https://yts.torrentbay.to/api/v2/{endpoint}.json?"
    
    for key, value in kwargs.items():
        url += f"{key}={value}&"

    print(url)
    res = requests.get(url)
    
    return res.json()
    
"""
Searches the Plex Movie library for the given title, taking into consideration different title formats with fuzzy mathcing.
    - Looks for an accuracy threshold of above 75% to consider a match. Can be adjusted optionally
        - Loljk, only looking for exact titles, fuck it
"""
def inPlexLibrary(title, accuracy=75):
    title = title.lower()
    for movie in plex_movies:
        # if fuzz.partial_ratio(title, movie.attributes['title'].value.lower()) >= 75:
        if title == movie.attributes['title'].value.lower():
            return True
    return False

def download(url):
    torbox_URL = f'http://{torbox_api_ip}:{torbox_port}/addTorrent'
    data = {
        'key': torbox_key,
        'url': url
    }
    res = requests.post(torbox_URL, json = data)

"""

"""
if __name__ == '__main__':

    print(f"# Movies: {len(plex_movies)}")
    for i, movie in enumerate(plex_movies):
        print(f"{i}: {movie.attributes['title'].value}")
    print(f"# Shows: {len(plex_shows)}")
    for i, show in enumerate(plex_shows):
        print(f"{i}: {show.attributes['title'].value}")

    # response_dict = yify("list_movies", quality="1080p", sort_by="download_count", limit=50, page=2)

    response_dict = yify("list_movies", quality="1080p", **dict(arg.split('=') for arg in sys.argv[1:]))
    movies = response_dict['data']['movies']
    for index, movie in enumerate(response_dict['data']['movies']):
        if not inPlexLibrary(movie['title']):
            # Checks if at end of list, and if not then checks if next movie is the same; for some reason the yts api sends duplicates sometimes
            if movies[-1] is not movie and movie['title'] == movies[index + 1]['title']:
                continue
            print(movie['title'])
            for torrent in movie['torrents']:
                # Only download 1080p torrents and prefer bluray over web
                if torrent['quality'] == '1080p' and (torrent['type'] == 'bluray' or torrent['type'] == 'web'):
                    # print(torrent['hash'])
                    download(torrent['url'])
                    break
            
    ...




