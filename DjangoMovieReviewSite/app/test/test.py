import requests
import socket
import random
from app import hidden_stuff

# request = requests.get("http://www.omdbapi.com/?i=" + id + "&plot=full&apikey=)
request = requests.get("http://www.omdbapi.com/?s=troop&type=movie&apikey=2377553f")
request2 = requests.get("http://www.omdbapi.com/?s='bird'&type=movie&page=1&apikey=2377553f")
# print(request2.text)

request = request.json()
request2 = request2.json()
query = 'car'

query = query.strip()

results = requests.get(
    "http://www.omdbapi.com/?s=" + query + "&type=movie&apikey=" + hidden_stuff.API_KEY)
results = results.json()

if ' ' in query:
   query = query.split(' ')

pages = round(int(results['totalResults']) / 10)
for p in range(int(pages)):
    p = p + 1
    p = str(p)
    r = requests.get(
    "http://www.omdbapi.com/?s=" + query + "&page=" + p + "&type=movie&apikey=" + hidden_stuff.API_KEY)
    r = r.json()
    for res in r['Search']:
        if res not in results['Search']:
            results['Search'].append(res)
    if p == str(5):
        break

'''if len(query) > 1:
    print('greater than 1')
    for q in query:
        r = requests.get(
            "http://www.omdbapi.com/?s=" + q + "&type=movie&apikey=" + hidden_stuff.API_KEY)
        r = r.json()
        if 'Search' in r and 'Error' not in r:
            for dict in r['Search']:
                results['Search'].append(dict)
        else:
            continue '''

print(results)

'''def backup_request(request1, request2):
    for dict in request2['Search']:
        request1['Search'].append(dict)

if 'Search' in request2 and 'Search' in request:
    backup_request(request2, request)

print(request)




results = requests.get(
           "http://www.omdbapi.com/?s=" + query[0] + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
       results = results.json()
       results2 = requests.get(
           "http://www.omdbapi.com/?s=" + query[1] + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
       results2 = results2.json()
       for dict in results2['Search']:
           results['Search'].append(dict)
           
                  if ' ' in query:
           query = query.split(' ')


           if len(query) > 1:
               results = requests.get(
                   "http://www.omdbapi.com/?s=" + query[
                       0] + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
               results = results.json()
               results2 = requests.get(
                   "http://www.omdbapi.com/?s=" + query[
                       1] + "&page=" + page + "&type=movie&apikey=" + hidden_stuff.API_KEY)
               results2 = results2.json()
               for dict in results2['Search']:
                   results['Search'].append(dict)
           info = results['Search']
           
           
           
        num_results = int(results.get('totalResults'))
       results_list_with_dups = results['Search']
       results_list = []
       for x in results['Search']:
           if x not in results_list:
               results_list.append(x)
       if num_results < 50:
           info = results_list[0:]
       else:
           info = results_list[0:50]
'''
