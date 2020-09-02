import requests
import http.client
from bs4 import BeautifulSoup

MetaUrl = 'https://flickmetrix.com/watchlist'

MetaHeaders =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# result = requests.get(MetaUrl, headers=MetaHeaders)

with open("Flick.html", "r") as f: #open the HTML file
    contents = f.read()

    html_soup = BeautifulSoup(contents, 'html.parser') #parse the contents of the html file that we've opened

    type(html_soup) #have no idea what this does

    movie_title, movie_date = html_soup.find_all('div', class_ = 'title ng-binding'), html_soup.find_all('div', class_ = 'film-section ng-binding') #double variable control

for i, j in zip(movie_title[::2], movie_date[::3]): # [::2] and [::3] iterates over every 2nd and 3rd element in each list respectively.
    title = i.text
    title = title.replace(" ", "+")
    title = title.replace(":", "%3A") #URL encoding for each title for a later POST request

    date = j.text #storing movie date into a variable for accurate search results
    date = date.replace("(", "")
    date = date.replace(")", "")
    #print(title, date)

    url = "https://api.themoviedb.org/3/search/movie?api_key=2b5c62f4ed3da916c3b4c6ca47003e46&language=en-US&page=1&include_adult=false&query={}&year={}".format(
        title, date)

    payload = "{}"
    response = requests.request("GET", url, data=payload)

    results = response.json()
    #print(results)

    if results["results"] and results["results"][0]["release_date"][:4] == date:

        movie_id = results["results"][0]["id"]

        conn = http.client.HTTPSConnection("api.themoviedb.org")

        payload = "{\"media_id\":%s}" % movie_id

        headers = {'content-type': "application/json;charset=utf-8"}

        conn.request("POST",
                     "/3/list/127145/add_item?api_key=2b5c62f4ed3da916c3b4c6ca47003e46&session_id=9ef3454015fb183f7611e6e510ff77bb52db2b74",
                     payload, headers)

        res = conn.getresponse()
        data = res.read()
        print(data)
        print("added:", title, date, "to your list")

    else:
        print(title, "was not added to your list because your code is crap!")



