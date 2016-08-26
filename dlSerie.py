import bs4
import requests
import transmissionrpc


url = ""

def dlSerie(name, season, episode):
    search = "{} S0{}E{}".format(name, season, episode)
    r_done = False
    while not r_done:
        r = requests.get("https://extratorrent.cc/search/?search={}".format(search))
        if r.status_code == 200:
            r_done = True
    name_with_point = name.replace(' ', '.')
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    for element in soup.find_all('td', {'class':u'tli'}):
        for link in element.find_all('a'):
            if name in link.text or name_with_point in link.text:
               url = link['href']
               break
    r_done = False
    while not r_done:
        r = requests.get("https://extratorrent.cc" + url)
        if r.status_code == 200:
            r_done = True
    tSoup = bs4.BeautifulSoup(r.text, "html.parser")
    img = tSoup.find('img', {'alt':u'Magnet link'})
    torrent = img.parent['href']
    print(torrent)
    tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="secret")
    tc.add_torrent("https://extratorrent.cc" + torrent)
