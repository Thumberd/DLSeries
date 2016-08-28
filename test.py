import requests

def get_episode(name, season, nEpisode):
    payload = {'api_key':  "ecab8308ea39b8e4f2d3e707d204f8b3", 'query': name}  # Finding infos about the show on the API
    findID = requests.get("http://api.themoviedb.org/3/search/tv", payload)
    idS = int(findID.json()['results'][0]['id'])
    payload = {'api_key':  "ecab8308ea39b8e4f2d3e707d204f8b3"}
    rEpisodes = requests.get("http://api.themoviedb.org/3/tv/{}/season/{}".format(idS, season), payload)
    episodes = rEpisodes.json()['episodes']
    for episode in episodes:
        if episode['episode_number'] == nEpisode:
            return episode

print(get_episode('NCIS', 12, 9))