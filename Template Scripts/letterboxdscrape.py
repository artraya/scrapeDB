import requests
import http.client
import json
from bs4 import BeautifulSoup
page = 3
addFailed = {}


while page <=11:

    MetaUrl = 'https://letterboxd.com/top10ner/list/2020-edition-top10ners-1001-greatest-movies/detail/page/{}/'.format(page)

    MetaHeaders =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(MetaUrl, headers=MetaHeaders)
    html_soup = BeautifulSoup(result.text, 'html.parser')
    type(html_soup)

    movieTitle, movieYear = html_soup.find_all('div', class_ = 'film-detail-content'), html_soup.find_all('small', class_='metadata')

    for i, j in zip(movieTitle,movieYear):
        title = i.h2.a.text
        year = j.a.text
        print(title,year)
        titleURLencode = title.replace(" ", "+")
        url = "https://api.themoviedb.org/3/search/movie?api_key=2b5c62f4ed3da916c3b4c6ca47003e46&language=en-US&page=1&include_adult=false&query={}&year={}".format(
            titleURLencode,year)

        response = requests.request("GET", url)

        results = response.json()

        if results["total_results"] >= 1:
            for i in range(results["total_results"]):
                try:
                    if results["results"][i]['title'] == title:

                        movie_id = results["results"][i]['id']

                        conn = http.client.HTTPSConnection("api.themoviedb.org")

                        payload = "{\"media_id\":%s}" % movie_id

                        headers = {'content-type': "application/json;charset=utf-8"}

                        conn.request("POST",
                                     "/3/list/141018/add_item?api_key=2b5c62f4ed3da916c3b4c6ca47003e46&session_id=9ef3454015fb183f7611e6e510ff77bb52db2b74",
                                     payload, headers)

                        res = conn.getresponse()
                        data = res.read()
                        print(data)
                    else:
                        print("couldn't add movie")
                        addFailed[title] = year
                except:
                    addFailed[title] = year
                    pass
        else:
            print('no results found')
            addFailed[title] = year
    page += 1


print(addFailed)



