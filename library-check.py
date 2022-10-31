import requests
import io
from xml.dom import minidom
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

token = '***REMOVED***'

res = requests.get(f"http://brokeserver.live:32400/library/sections/1/all?X-Plex-Token={token}")
file = io.StringIO(res.text)
xml = minidom.parse(file)
movies = xml.getElementsByTagName('Video')

res = requests.get(f"http://brokeserver.live:32400/library/sections/2/all?X-Plex-Token={token}")
file = io.StringIO(res.text)
xml = minidom.parse(file)
shows = xml.getElementsByTagName('Directory')

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
"""
def inPlexLibrary(title, accuracy=75):
    title = title.lower()
    for movie in movies:
        if fuzz.partial_ratio(title, movie.attributes['title'].value.lower()) >= 75:
            return True
    return False

    

if __name__ == '__main__':

    print(f"# Movies: {len(movies)}")
    for i, movie in enumerate(movies):
        print(f"{i}: {movie.attributes['title'].value}")
    print(f"# Shows: {len(shows)}")
    for i, show in enumerate(shows):
        print(f"{i}: {show.attributes['title'].value}")

    response_dict = yify("list_movies", sort_by="download_count", limit=50)
    for movie in response_dict['data']['movies']:
        if not inPlexLibrary(movie['title']):
            print(movie['title'])
            
    ...




