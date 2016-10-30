from celery import Celery
from celery.schedules import crontab
from celery.decorators import periodic_task
import transmissionrpc
import requests
import subAndRename

app = Celery('worker', broker='amqp://guest@localhost//')

def send_sms(text):
    r = requests.get("https://smsapi.free-mobile.fr/sendmsg?user=10908880&pass=9o83gNpCCAMjjs&msg={}".format(text))

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
                    subAndRename.fetch_episode(file_name, "/home/media/USBHDD1/NASRPI/Series")
            torrent.stop()
