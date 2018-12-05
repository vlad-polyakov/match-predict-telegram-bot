import requests, bs4
import xml.etree.ElementTree as xml
from http.server import HTTPServer, CGIHTTPRequestHandler

names = []
smth = []
#info = [[],[]]
info = [[0 for j in range(0, 10)] for i in range(0, 100)]
searchList = []
searchListCoefs =[]
def createParser(url):
    s=requests.get(url)
    b=bs4.BeautifulSoup(s.text, "html.parser")
    return b


def setInfo(bs):
    allElements = bs.find_all("tbody", {"class":"bg"})
    for index in range(0,len(allElements)):
        names.append(allElements[index]['data-event-name'])
        #coefs1 = allElements[index].find_all("span")
        qqqq = allElements[index].find_all("span", {"class":"selection-link normal "})
        for j in range (0,len(qqqq)):
            info[index][j]=qqqq[j]['data-selection-price']

def createXML(filename, info, names):
    if open(filename, 'w')!=None:
        open(filename, 'w').close()
    root = xml.Element("Info")
    for index in range(0,len(names)):
        appt = xml.Element("match")
        root.append(appt)

    # создаем дочерний суб-элемент.
        matchnameTag = xml.SubElement(appt, "match name")
        matchnameTag.text = names[index]
        firstWonTag = xml.SubElement(appt, "1")
        firstWonTag.text = info[index][0]

        nobodyWonTag = xml.SubElement(appt, "X")
        nobodyWonTag.text = info[index][1]

        secondWonTag = xml.SubElement(appt, "2")
        secondWonTag.text = info[index][2]

        firstOrNbdTag = xml.SubElement(appt, "1X")
        firstOrNbdTag.text = info[index][3]

        firstOrSecondTag = xml.SubElement(appt, "12")
        firstOrSecondTag.text = info[index][4]

        secondOrNbdTag = xml.SubElement(appt, "X2")
        secondOrNbdTag.text = info[index][5]

        tree = xml.ElementTree(root)
        tree.write(open(filename, 'w'), encoding="unicode")
"""server_address = ("", 8000)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()"""

def findTeam(team):
    j=0
    for index in range(0,len(names)):
        coefs = []
        pos = names[index].find(team)
        if pos != -1:
            searchList.append(names[index])
            coefs.append(info[index][0])
            coefs.append(info[index][2])
            searchListCoefs.append(coefs)


def Parser(team):
    bs = createParser('https://www.marathonbet.by/su/betting/Football/?menu=11')
    setInfo(bs)
    createXML("marafon.xml",info,names)
    findTeam(team)
    massiv = []
    for index in range (0,len(searchList)):
        pair = []
        pair.append(searchList[index])
        pair.append(searchListCoefs[index])
        massiv.append(pair)
    return massiv





