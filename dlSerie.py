import bs4
import requests
import transmissionrpc

tc = transmissionrpc.Client('localhost', port=9091, user="transmission", password="secret")

url = ""

def dlSerie(name, season, episode):
    search = "{} S0{}E{}".format(name, season, episode)
    r = requests.get("https://extratorrent.cc/search/?search={}".format(search))
    name_with_point = name.replace(' ', '.')
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    for element in soup.find_all('td', {'class':u'tli'}):
        print(element)
        for link in element.find_all('a'):
            if name in link.text or name_with_point in link.text:
                if "x264" in link.text:
                   url = link['href']
                   break

    r = requests.get("https://extratorrent.cc" + url)
    tSoup = bs4.BeautifulSoup(r.text, "html.parser")
    img = tSoup.find('img', {'src':u'//images4et.com/images/magnet.gif'})
    torrent = img.parent['href']
    print(torrent)
    tc.add_torrent("https://extratorrent.cc" + torrent)
