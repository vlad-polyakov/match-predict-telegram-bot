import telebot
import parser as p
import numpy as np
from sklearn import linear_model
import csv
import requests, bs4
import xml.etree.ElementTree as xml
from http.server import HTTPServer, CGIHTTPRequestHandler
names = []
smth = []
A = ''
B = ''
coef1 = []
coef2 = []
#info = [[],[]]
info = [[0 for j in range(0, 10)] for i in range(0, 100)]
searchList = []
searchListCoefs =[]

# main variables
TOKEN = "704831511:AAGOlHJgQ-y0cJ58VuNg0fY-3d_x-POiRqc"
bot = telebot.TeleBot(TOKEN)


###

###   PARSER

###
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Введите название команды на русском')
    bot.register_next_step_handler(msg, askAge)


def askAge(message):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Выбранная команда: "' + text + '".')
    string = ""
    massiv = Parser(text)
    for index in range(0,len(massiv)):
        indexStr = str(index+1)
        string2 = "Матч " + indexStr + ": " + massiv[index][0]
        msg = bot.send_message(chat_id, string2)
        a=massiv[index][1][0]
        b=massiv[index][1][1]
        string = "Победа 1: " + a + ", Победа 2: " +b
        msg = bot.send_message(chat_id, string)
        coef1.append(float(a))
        coef2.append(float(b))
        

@bot.message_handler(func=lambda message: True, content_types=['text'])
def start_handler(message):
    chat_id = message.chat.id
    text = message.text
    ver1 =100 - coef1[0]*1.3*10
    ver2 =100 - coef2[0]*1.3*10
    string = "Вероятность победы первой команды: "+str(ver1) + " %, Вероятность победы второй команды: "+str(ver2)+" %"
    msg = bot.send_message(chat_id, string)
    bot.register_next_step_handler(msg, start_handler2)
    A= message.text

def start_handler2(message):
    chat_id = message.chat.id
#    text = message.text
    msg = bot.send_message(chat_id, 'Введите название команды 2 eng')
    B= message.text
#    bot.register_next_step_handler(msg, main)
    if A != '' and B != '':
       m = main(A, B)
       print(m)


# Чтение из csv файла
def main(A = 'Valencia', B='Sevilla'):
    def csv_parser(filename):
        x, y, = list(), list()
        # A, B = input(), input()
        # A, B = 'Valencia', 'Sevilla'
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                if (row[4] == A and row[5] == B):
                    x.append(int(row[6]))
                    y.append(int(row[7]))
                elif (row[4] == B and row[5] == A):
                         x.append(int(row[7]))
                         y.append(int(row[6]))
        return x, y


    x, y = csv_parser('FMEL_Dataset.csv')

    # Построение линейной модели

    linear = linear_model.LinearRegression()
    trainX = np.asarray(x[20:len(x)]).reshape(-1, 1)
    trainY = np.asarray(y[20:len(y)]).reshape(-1, 1)
    testX = np.asarray(x[:20]).reshape(-1, 1)
    testY = np.asarray(y[:20]).reshape(-1, 1)
    linear.fit(trainX, trainY)
    linear.score(trainX, trainY)

    # Параметры модели(вещь не особо нужная применительно к нашему проекту, можно спокойно коментить)

    """print('Coefficient: \n', linear.coef_)
    print('Intercept: \n', linear.intercept_)
    print('R² Value: \n', linear.score(trainX, trainY))"""

    # Предсказания модели (представляет из себя набор вероятностей)

    First_team_score = linear.predict(testX) # сколько забьет первая команда
    Second_team_score = linear.predict(testY) # сколько забьет вторая команда

    #Сумма массива

    def listsum(numlist):
        sum = 0
        for i in numlist:
            sum = sum + i
        return sum

    #Чтоб не сравнивать каждый элемент массива, будем сравнивать среднее

    chanse_to_win_first = listsum(First_team_score)/len(First_team_score)
    chanse_to_win_second = listsum(Second_team_score)/len(Second_team_score)

    if chanse_to_win_first > chanse_to_win_second:
        print("First team won")
        return 1
    elif chanse_to_win_first == chanse_to_win_second:
        print("Draw")
        return 0
    else:
        print("Second team won")
        return -1
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




###

###   ANALYTIC

###


if __name__ == '__main__':
    bot.polling(none_stop=True)