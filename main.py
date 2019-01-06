# all my imports
import requests
from bs4 import BeautifulSoup
import json
import re

def title(bs):
    title = bs.title.text
    return title

def description(bs):
    description = bs.find('div','summary_text').text.strip()
    return description

def rating(bs):
    rating = json.loads(bs.find('script', type='application/ld+json').text)['contentRating']
    return rating

def value(bs):
    value = json.loads(bs.find('script', type='application/ld+json').text)['aggregateRating']['ratingValue']
    return value

def actors(x):
    actors_list = []
    # actors = json.loads(x.find('script', type='application/ld+json').text)['actor']
    # for actor in actors:
    #     actors_list.append(str(actor['name']))

    all_actors = x.find('table',class_='cast_list').find_all('a',href = re.compile(r'/name/*'))
    # print(all_actors)
    for actor in all_actors:
        data = actor.getText().strip()
        if len(data) != 0:
            actors_list.append(data) 
    return actors_list

def directors(x):
	directors = json.loads(x.find('script', type='application/ld+json').text)['director']
	directors_list = []
	for director in directors:
		directors_list.append(str(director['name']))
	return directors_list

def movie(id):
    # get web page 
    r = requests.get("https://www.imdb.com/title/{0}/".format(id))

    r_unparsed = r.text

    bs = BeautifulSoup(r_unparsed,'lxml')
    # print(bs)
    
    info = {}
    info['id'] = id
    info['title'] = title(bs)
    info['description'] = description(bs)
    info['rating'] = rating(bs)
    info['actors'] = actors(bs)
    info['directors'] = directors(bs)
    info['value'] = value(bs)

    return info


if __name__ == "__main__":
    movie_id = "tt4154756"
    response = movie(movie_id)
    print(response)
