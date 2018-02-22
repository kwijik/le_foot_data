import pandas as pd
import numpy as np
import urllib.request as urllib2
import hashlib
import sqlite3
from time import strptime, strftime

conn = sqlite3.connect('seasons.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS known_url(url VARCHAR(255) PRIMARY KEY, hash VARCHAR(255))")

cur.execute("CREATE TABLE IF NOT EXISTS season(id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(255), dt DATE, home_team VARCHAR(255), away_team VARCHAR(255), fthg  INTEGER, ftag INTEGER, nmseason INTEGER)")


site = "http://www.football-data.co.uk/mmz4281"
seasons = []
numberOfSeasons = 10

year = 18
for i in range(numberOfSeasons):
    year -= 1
    url =site + '/' + "{:02d}".format(year) +  "{:02d}".format(year+1) + '/D1.csv'
    print(url)
    data = urllib2.urlopen(url) #запрос
    hash = hashlib.md5(data.read()).hexdigest() # читае read, хешируем и получаем hexdigest
    # хотим получить хеш данных которые пришли с сервера
    # надо преобразовать байты в строку
    #	Just for the understanding: read() of urlopen() returns bytes. decode() will covert the bytes to a unicode string. And md5() requires bytes as input
    # cur = conn.cursor()
    cur.execute("SELECT count(*) FROM known_url WHERE url=? AND hash=?", (url, hash,))
    rows = cur.fetchall()
    print(rows) # можно запросить header файла и в header должен быть hash
    if(rows[0][0] == 1):
        continue
    cur.execute("DELETE FROM known_url WHERE url=?" , (url,))
    cur.execute("DELETE FROM season WHERE url=?" , (url,))

    cur.execute("INSERT INTO known_url(url,hash) VALUES(?,?)",(url,hash,))

    season = pd.read_csv(url, header=0, sep=',')
    #print(season["HomeTeam"][0])
    for s in range(len(season)):
        print("S: {0}, Type: {1}".format(season["FTHG"][s].item(),type(season["FTHG"][s].item())))
        dt = strptime(season["Date"][s], "%d/%m/%y")
        dt = strftime("%Y-%m-%d", dt)
        cur.execute("INSERT INTO season(url, dt, home_team, away_team, fthg, ftag, nmseason) VALUES(?,?,?,?,?,?, ?)",\
                    (url,dt,season["HomeTeam"][s], season["AwayTeam"][s], season["FTHG"][s].item(), season["FTAG"][s].item(), year))

   #  data.read()
    #seasons.append(season[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]) нет смысла, тк записали в базу

conn.commit()

conn.close()
