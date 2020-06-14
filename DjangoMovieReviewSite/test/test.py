import requests
import socket

#request = requests.get("http://www.omdbapi.com/?i=" + id + "&plot=full&apikey=)
#request = requests.get("http://www.omdbapi.com/?s=lighthouse&type=movie&apikey=2377553f")
request2 = requests.get("http://www.omdbapi.com/?s='aaaaaaa'&type=movie&apikey=2377553f")
#print(request2.text)
print(request2.text)


