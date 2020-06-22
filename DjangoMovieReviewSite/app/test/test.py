import requests
import socket
from app import hidden_stuff

#request = requests.get("http://www.omdbapi.com/?i=" + id + "&plot=full&apikey=)
#request = requests.get("http://www.omdbapi.com/?s=lighthouse&type=movie&apikey=")
request2 = requests.get("http://www.omdbapi.com/?t='Birdman'&type=movie&page=1&apikey=" + hidden_stuff.api_key)
#print(request2.text)
print(request2.text)


