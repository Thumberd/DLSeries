import sqlite3
import requests
from datetime import datetime

class Serie:
    def __init__(self, name, season=0, episode=0):
        self.conn = sqlite3.connect('series.sqlite')
        self.c = self.conn.cursor()
        self.themovieDBKey = "ecab8308ea39b8e4f2d3e707d204f8b3"
        try:
            idS = int(name)
        except ValueError:
            self.c.execute("""SELECT * FROM series WHERE name = ?""", (name,))
            self.serie = self.c.fetchone()
        else:
            self.c.execute("""SELECT * FROM series WHERE id = ?""", (idS,))
            self.serie = self.c.fetchone()
        if self.serie == None:
            payload = {'api_key': self.themovieDBKey, 'query': name}  # Finding infos about the show on the API
            findID = requests.get("http://api.themoviedb.org/3/search/tv", payload)
            idS = int(findID.json()['results'][0]['id'])
            if season == 0:
                payload = {'api_key': self.themovieDBKey}
                findSeasons = requests.get("http://api.themoviedb.org/3/tv/" + str(idS), payload)
                lastSeason = findSeasons.json()['seasons'][-1]
                #Got the last season, now trying to get the last episode
                payload = {"api_key": self.themovieDBKey}
                rEpisodes = requests.get(
                    "http://api.themoviedb.org/3/tv/" + str(idS) + "/season/" + str(lastSeason['season_number']),
                    payload)
                episodes = rEpisodes.json()['episodes']
                #Looping in the last season's episodes to find the last aired
                now = datetime.now().date()

                for episode in episodes:
                    air_date = datetime(int(episode['air_date'][0:4]), int(episode['air_date'][5:7]),
                                        int(episode['air_date'][8:10])).date()
                    diff = air_date - now
                    if diff.total_seconds() < 0:
                        lastEpisode = episode
                        continue
                    else:
                        break
                print("I know the show is {}, the last season is {} and the last episode is {}, number {}".format(
                    name, lastSeason['season_number'], lastEpisode['name'], lastEpisode['episode_number']))
                self.c.execute("""INSERT INTO series(name, api_id, season, episode) VALUES (?, ?, ?, ?)""",
                               (name, idS, int(lastSeason['season_number']), int(lastEpisode['episode_number'])))
                self.conn.commit()
                self.c.execute("""SELECT * FROM series WHERE name = ?""", (name,))
                self.serie = self.c.fetchone()

    def isNewEpisodeAired(self):
        payload = {'api_key': self.themovieDBKey}
        findSeasons = requests.get("http://api.themoviedb.org/3/tv/" + str(self.serie[2]), payload)
        lastSeason = findSeasons.json()['seasons'][-1]
        # Got the latest season, now get the episode aired recently
        payload = {"api_key": self.themovieDBKey}
        rEpisodes = requests.get(
            "http://api.themoviedb.org/3/tv/" + str(self.serie[2]) + "/season/" + str(lastSeason['season_number']),
            payload)
        episodes = rEpisodes.json()['episodes']

        now = datetime.now().date()
        nSeason = self.serie[3]
        nEpisode = self.serie[4]
        for episode in episodes:
            air_date = datetime(int(episode['air_date'][0:4]), int(episode['air_date'][5:7]),
                                int(episode['air_date'][8:10])).date()
            diff = now - air_date
            if diff.days < 6 and diff.days > 0:
                nSeason = lastSeason['season_number']
                nEpisode = episode['episode_number']
                break
        if self.serie[3] == nSeason and self.serie[4] == nEpisode:
            return False
        else:
            self.c.execute("""UPDATE series SET season = ? AND episode = ? WHERE id = ?""",
                           (nSeason, nEpisode, self.serie[0]))
            self.conn.commit()
            return True