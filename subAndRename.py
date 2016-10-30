import requests
import re
import os
import sys

key = "**"
base_format_file = "{show} - {season}x{episode} - {name}.{extension}"


def sub(idE, path):
    rSearch = requests.get("https://api.betaseries.com/subtitles/episode?key={}&id={}".format(key, idE))
    link = rSearch.json()['subtitles'][0]['url']
    rSub = requests.get(link)
    if rSub.status_code == 200:
        if path != "":
            with open(path, 'wb') as f:
                for chunk in rSub.iter_content(1024):
                    f.write(chunk)
        else:
            return rSub.text
    return  rSub.status_code


def get_episode(name, season, n_episode):
    findID = requests.get("https://api.betaseries.com/shows/search?key={}&title={}".format(key, name))
    idS = int(findID.json()['shows'][0]['id'])
    rEpisodes = requests.get("https://api.betaseries.com/episodes/search?key={}&show_id={}&number=S{}E{}"
                             .format(key, idS, season, n_episode))
    episode = rEpisodes.json()['episode']
    return episode


def get_show(name):
    name = name.replace('.', ' ')
    list = ["NCIS Los Angeles", 'NCIS', "The 100", "Quantico", "Blacklist", "Mr  Robot", "Mr Robot"]
    for show in list:
        if show in name:
            return show
    return None


def rename_files(previous_video_file, future_video_file, base_path=os.getcwd()):
    try:
        os.rename(base_path + '/' + previous_video_file, base_path + '/' + future_video_file)
    except Exception as e:
        return e
    else:
        return None


def fetch_episode(file_name, dest_path = None):
    match_season = re.search(r'S([0-9])+', file_name)
    match_episode = re.search(r'E([0-9])+', file_name)
    if match_season and match_episode:
        season = file_name[match_season.start()+1:match_season.end()]
        episode = file_name[match_episode.start()+1:match_episode.end()]
    else:
        match = re.search(r'([0-9])+x([0-9])+', file_name)
        season = file_name[match.start() :match.start()+2]
        episode = file_name[match.start() + 3:match.end()]
    if season != "" and episode != "":
        show = get_show(file_name)
        episodeInfo= get_episode(show, season, episode)
        name = base_format_file.format(show=show, season=season, episode=episode, name=episodeInfo['title'],
                                       extension=file_name.split('.')[-1])
        srt_name = base_format_file.format(show=show, season=season, episode=episode, name=episodeInfo['title'],
                                           extension='srt')
        sub(episodeInfo['id'], os.getcwd() + '/' + srt_name)
        if dest_path != None:
            rename_files(file_name, name, dest_path)
        else:
            rename_files(file_name, name)