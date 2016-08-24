from celery import Celery
import transmissionrpc

app = Celery('worker', broker='amqp://guest@localhost//')

@@periodic_task(run_every=crontab(minute='*'))
def checkForDownloadedFiles():
    tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="secret")
    torrents = tc.get_torrents()
    for torrent in torrents:
        if torrent.status != "downloading":
            print("Done")
