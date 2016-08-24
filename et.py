import bs4
import requests
import transmissionrpc

tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="secret")

SEARCH = "The 100 S03E14;"

r = requests.get("https://extratorrent.cc/search/?search={}".format(SEARCH))

soup = bs4.BeautifulSoup(r.text, "html.parser")
for element in soup.find_all('td', {'class':u'tli'}):
    for link in element.find_all('a'):
        if "The 100" in link.text or "The.100" in link.text:
            if "x264" in link.text:
               url = link['href']
               break

r = requests.get("https://extratorrent.cc" + url)
tSoup = bs4.BeautifulSoup(r.text, "html.parser")
img = tSoup.find('img', {'src':u'//images4et.com/images/download_normal.gif'})
torrent = img.parent['href']
print(torrent)
tc.add_torrent("https://extratorrent.cc" + torrent)