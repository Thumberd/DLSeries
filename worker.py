from celery import Celery
from celery.schedules import crontab
from celery.decorators import periodic_task
import transmissionrpc
import shutil
import os
import hashlib
import requests
import re

app = Celery('worker', broker='amqp://guest@localhost//')


def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def sub(hash, path):
    print(hash)
    headers = {
        'User-Agent': "SubDB/1.0 (DomoPi/1.0; http://rpialbrecht.ddns.net)"
    }
    payload = {
        'action': 'download',
        'hash': hash
    }
    rSearch = requests.get("http://api.thesubdb.com/", headers=headers, params=payload, stream=True)
    if rSearch.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in rSearch.iter_content(1024):
                f.write(chunk)


def send_sms(text):
    r = requests.get("https://smsapi.free-mobile.fr/sendmsg?user=10908880&pass=9o83gNpCCAMjjs&msg={}".format(text))


def get_show(name):
    name = name.replace('.', ' ')
    list = ["NCIS Los Angeles", 'NCIS', "The 100", "Quantico", "Blacklist", ]
    for show in list:
        if show in name:
            return show


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


@periodic_task(run_every=crontab(minute='*'))
def checkForDownloadedFiles():
    tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="secret")
    torrents = tc.get_torrents()
    for torrent in torrents:
        if torrent.status != "downloading" and torrent.status != "stopped":
            files = torrent.files()
            i = 0
            for i in range(0, len(files)):
                file_name = files[i]['name']
                if file_name.split('.')[-1] != 'txt':
                    matchSeason = re.search(r'S([0-9])+', file_name)
                    if matchSeason:
                        season = file_name[matchSeason.start():matchSeason.end()]
                    matchEpisode = re.search(r'E([0-9])+', file_name)
                    if matchEpisode:
                        episode = file_name[matchSeason.start():matchSeason.end()]
                    show = get_show(file_name)
                    episodeInfo = get_episode(show, season, episode)
                    name = "{show} - {season}x{episode} - {name}.{extension}".format(show=show, season=season, episode=episode, name=episodeInfo['name'],
                                                                                     extension=file_name.split('.')[-1])
                    srt_name = "{show} - {season}x{episode} - {name}.{extension}".format(show=show, season=season, episode=episode, name=episodeInfo['name'],
                                                                                     extension='srt')
                    os.system('sudo mv /var/lib/transmission-daemon/downloads/' + file_name + ' /media/USBHDD1/NASRPI/Series/' + name)
                    path = '/media/USBHDD1/NASRPI/Series/' + name
                    hash = get_hash(path)
                    sub(hash, path + '.srt')
                    os.system('sudo mv ' + path + '.srt ' + srt_name)
            torrent.stop()
