from celery import Celery
from celery.schedules import crontab
from celery.decorators import periodic_task
import transmissionrpc
import shutil
import os
import hashlib
import requests

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


@periodic_task(run_every=crontab(minute='*'))
def checkForDownloadedFiles():
    print('Do It Right')
    tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="secret")
    torrents = tc.get_torrents()
    for torrent in torrents:
        if torrent.status != "downloading" and torrent.status != "stopped" or 1 == 1:
            files = torrent.files()
            i = 0
            for i in range(0, len(files)):
                if files[i]['name'].split('.')[-1] != 'txt':
                    os.system('sudo mv /var/lib/transmission-daemon/downloads/' + files[i]['name'] + ' /media/USBHDD1/NASRPI/Series/' + files[i]['name'].split('/')[1])
                    path = '/media/USBHDD1/NASRPI/Series/' + files[i]['name'].split('/')[1]
                    print(path)
                    hash = get_hash(path)
                    print(hash)
                    sub(hash, path + '.srt')
            torrent.stop()
