import requests
from xml.dom import minidom

token = '***REMOVED***'

res = requests.get(f"http://brokeserver.live:32400/library/sections/1/all?X-Plex-Token=${token}")
xml = minidom.parse(res.text)
movies = xml.getElementsByTagName('Video')

res = requests.get(f"http://brokeserver.live:32400/library/sections/2/all?X-Plex_token=${token}")
xml = minidom.parse(res.text)
shows = xml.getElementsByTagName('Video')

print(f"# Movies: ${len(movies)}")
print(f"# Shows: ${len(shows)}")

