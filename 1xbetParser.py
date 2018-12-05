import requests, bs4
import xml.etree.ElementTree as xml
names = []
smth = []
#info = [[],[]]
info = [[0 for j in range(0, 6)] for i in range(0, 1000)]

def createParser(url):
    s=requests.get(url)
    b=bs4.BeautifulSoup(s.text, "html.parser")
    return b
        

def setInfo(bs):
    allElements = bs.find_all("span", {"class":"c-events__teams"})
    allCoefs = []
    for index in range(0,len(allElements)):
        names.append(allElements[index].text.strip())
    allGroupCoefs = bs.find_all("div",{"class":"c-bets"})
    for index in range(0,len(allGroupCoefs)):
        allCoefs.append(allGroupCoefs[index].find_all("a",{"class":"c-bets__bet c-bets__bet_coef c-bets__bet_sm "}))
        for j in range(0,6):
            if allCoefs[index] != []:
                info[index][j] = allCoefs[index][j].text.strip()
    for index in range(0,100):
        if info[index][0] == 0:
            del(info[index])
            index -=1
    

def createXML(filename):
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
    
def main():
    bs = createParser('https://1xbet.com/by/line/Football/')
    setInfo(bs)
    createXML("1xbet.xml")
main()