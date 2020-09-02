import requests
import http.client
from bs4 import BeautifulSoup
import math

#MetaUrl = 'https://flickmetrix.com/watchlist'

MetaHeaders =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# result = requests.get(MetaUrl, headers=MetaHeaders)

with open("EbertHTM.html", "r", encoding="utf-8") as f: #open the HTML file
    contents = f.read()

    html_soup = BeautifulSoup(contents, 'html.parser') #parse the contents of the html file that we've opened

    type(html_soup) #have no idea what this does

    movie_title, movie_date = html_soup.find_all('div', class_ = 'great-movie-list'), html_soup.find_all('td', class_ = 'g-year') #double variable control

   # movie_score = html_soup.find_all('div', class_ = 'megascore ng-binding')

added_movies = []
unadded_movies = []


for i, j in zip(movie_title, movie_date):


    title = i.text

    title = title.replace(" ", "+")
    title = title.replace(":", "%3A") #URL encoding for each title for a later POST request
    date = j.text

    url = "https://api.themoviedb.org/3/search/movie?api_key=2b5c62f4ed3da916c3b4c6ca47003e46&language=en-US&page=1&include_adult=false&query={}&year={}".format(
        title, date)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    results = response.json()
    print(results)
    print(results['results'][0]["original_title"])

   # if results["results"] and results["results"][0]["release_date"][:4] == date:
        #print(title, date)

        # added_movies.append("{} ({})".format(title, date))
        #
        # # print(added_movies)
        #
        # movie_id = results["results"][0]["id"]
        #
        # conn = http.client.HTTPSConnection("api.themoviedb.org")
        #
        # payload = "{\"media_id\":%s}" % movie_id
        #
        # headers = {'content-type': "application/json;charset=utf-8"}
        #
        # conn.request("POST",
        #              "/3/list/127191/add_item?api_key=2b5c62f4ed3da916c3b4c6ca47003e46&session_id=9ef3454015fb183f7611e6e510ff77bb52db2b74",
        #              payload, headers)
        #
        # res = conn.getresponse()
        # data = res.read()
        # print(data)



    # else:
    #     print(title, date, " <-  Could not find this one. Noted!")
    #     unadded_movies.append("{} ({})".format(title, date))

#print(added_movies, "\n")
#print(unadded_movies, )