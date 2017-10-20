from flask import Flask, render_template,request, Response
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os, time, glob
import seaborn as sns
import base64
import numpy as np
import sqlite3



#instantiate the flask app
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    conn = sqlite3.connect('data_app/seasons.db')

    df = pd.read_sql(sql='select * from season', con=conn)
    #df = pd.read_csv('http://www.football-data.co.uk/mmz4281/1718/D1.csv', header=0, sep=',')

    list_of_teams = df["home_team"].unique()


    #return render_template("index.html", table = df1.head().to_html(), path = plotfile, teams = list_of_teams)
    return render_template("index.html", teams = list_of_teams)
"""
@app.route("/get_table")
def get_table():
    conn = sqlite3.connect('data_app/seasons.db')

    team1 = request.values.get('team1')
    team2 = request.values.get('team2')
    print(team2, team1)
    #df1 = pd.read_csv('http://www.football-data.co.uk/mmz4281/1718/D1.csv', header=0, sep=',')

    df = pd.read_sql(sql='SELECT * from season WHERE home_team=? OR away_team=? OR home_team=? OR away_team=?', con=conn, params=(team1, team1,team2,team2,))

    return df.to_html()
"""


@app.route("/duel_table")
def duel_table():
    conn = sqlite3.connect('data_app/seasons.db')

    team1 = request.values.get('team1')
    team2 = request.values.get('team2')
    #df1 = pd.read_csv('http://www.football-data.co.uk/mmz4281/1718/D1.csv', header=0, sep=',')

    df = pd.read_sql(sql='SELECT * from season WHERE home_team=? OR away_team=? OR home_team=? OR away_team=?', con=conn, params=(team1, team1,team2,team2,))
    selected_columns = ["home_team", "away_team", "fthg", "ftag", "nmseason"]
    df = df[selected_columns]
    df = df[((df.home_team ==team1) | (df.away_team == team1)) & ((df.home_team ==team2) | (df.away_team == team2))]
    return df.to_html(index=False)


@app.route("/last_games_team1")
def last_games_team1():
    conn = sqlite3.connect('data_app/seasons.db')

    team1 = request.values.get('team1')
    team2 = request.values.get('team2')

    df = pd.read_sql(sql='SELECT dt,home_team,away_team,fthg,ftag,nmseason from season WHERE (home_team=? OR away_team=?) and nmseason=(SELECT MAX(nmseason) FROM season)', con=conn, params=(team1, team1))
    #selected_columns = ["dt","home_team", "away_team", "fthg", "ftag", "nmseason"]
    #df = df[selected_columns]
   # df = df[((df.home_team ==team1) | (df.away_team == team1)) & ((df.home_team ==team2) | (df.away_team == team2))]
    return df.to_html(index=False)

@app.route("/last_games_team2")
def last_games_team2():
    conn = sqlite3.connect('data_app/seasons.db')

    team1 = request.values.get('team1')
    team2 = request.values.get('team2')
    df = pd.read_sql(sql='SELECT dt,home_team,away_team,fthg,ftag,nmseason  from season WHERE (home_team=? OR away_team=?) and nmseason=(SELECT MAX(nmseason) FROM season)', con=conn, params=(team2, team2))
    #selected_columns = ["dt", "home_team", "away_team", "fthg", "ftag", "nmseason"]  #df = df[selected_columns]
    return df.to_html(index=False)


@app.route("/rating_table")
def rating_table():
    conn = sqlite3.connect('data_app/seasons.db')

    team1 = request.values.get('team1')
    team2 = request.values.get('team2')
    print(team2, team1)
    #df1 = pd.read_csv('http://www.football-data.co.uk/mmz4281/1718/D1.csv', header=0, sep=',')

    df = pd.read_sql(sql='SELECT * from season WHERE home_team=? OR away_team=? OR home_team=? OR away_team=? ORDER BY nmseason', con=conn, params=(team1, team1,team2,team2,))

    seasons_tableau = df["nmseason"].unique()
    dict_res = {}
    teams = [team1, team2]
    for team in teams:
        arr = []
        for s in seasons_tableau:
            goals_for = df[(df["home_team"] == team) & (df["nmseason"] == s)]["fthg"].sum() + \
                        df[(df["away_team"] == team) & (df["nmseason"] == s)]["ftag"].sum()
            goals_against = df[(df["home_team"] == team) & (df["nmseason"] == s)]["ftag"].sum() + \
                            df[(df["away_team"] == team) & (df["nmseason"] == s)]["fthg"].sum()
            number_of_games = len(df[((df["home_team"] == team) | (df["away_team"] == team)) & (df["nmseason"] == s)])
            if number_of_games != 0:
                rate = (goals_for - goals_against) / number_of_games
            else:
                rate = 0
            arr.append(rate)
        dict_res[team] = arr
    df2 = pd.DataFrame(dict_res, index=seasons_tableau, columns=teams)

    return df2.to_html()


@app.route("/positional_rating_table")
def positional_rating_table():
    conn = sqlite3.connect('data_app/seasons.db')

    home = request.values.get('team1') # team1 из js
    away = request.values.get('team2')
    df = pd.read_sql(
        sql='SELECT * from season WHERE home_team=? OR away_team=?  ORDER BY nmseason',
        con=conn, params=(home, away,))
    print(df[df.nmseason == 11])
    seasons_tableau = df["nmseason"].unique()
    dict_res = {}
    teams = [home, away]

    dict_res1 = {}
    arr = []
    for s in seasons_tableau:
        goals_for = df[(df["home_team"] == home) & (df["nmseason"] == s)]["fthg"].sum()
        goals_against = df[(df["home_team"] == home) & (df["nmseason"] == s)]["ftag"].sum()
        number_of_games = len(df[(df["home_team"] == home) & (df["nmseason"] == s)])
        if number_of_games != 0:
            rate = (goals_for - goals_against) / number_of_games
        else:
            rate = 0
        arr.append(rate)
    dict_res1[home] = arr

    arr = []
    for s in seasons_tableau:
        goals_for = df[(df["away_team"] == away) & (df["nmseason"] == s)]["ftag"].sum()
        goals_against = df[(df["away_team"] == away) & (df["nmseason"] == s)]["fthg"].sum()
        number_of_games = len(df[(df["away_team"] == away) & (df["nmseason"] == s)])
        if number_of_games != 0:
            rate = (goals_for - goals_against) / number_of_games
        else:
            rate = 0
            # print("For:{}, Against:{}, games:{}, seasom:{}, rate:{}".format(goals_for, goals_against, number_of_games, s,rate))
        arr.append(rate)
    dict_res1[away] = arr

    df3 = pd.DataFrame(dict_res1, index=seasons_tableau, columns=teams)
    return df3.to_html()


@app.route("/get_rating")

def get_rating():
    conn = sqlite3.connect('data_app/seasons.db')

    team1 = request.values.get('team1')
    team2 = request.values.get('team2')
    print(team2, team1)
    #df1 = pd.read_csv('http://www.football-data.co.uk/mmz4281/1718/D1.csv', header=0, sep=',')

    df = pd.read_sql(sql='SELECT * from season WHERE home_team=? OR away_team=? OR home_team=? OR away_team=? ORDER BY nmseason', con=conn, params=(team1, team1,team2,team2,))
    seasons_tableau = df["nmseason"].unique()
    dict_res = {}
    teams = [team1,team2]
    for team in teams:
        arr = []
        for s in seasons_tableau:
            goals_for = df[(df["home_team"] == team) & (df["nmseason"] == s)]["fthg"].sum() + \
                        df[(df["away_team"] == team) & (df["nmseason"] == s)]["ftag"].sum()
            goals_against = df[(df["home_team"] == team) & (df["nmseason"] == s)]["ftag"].sum() + \
                            df[(df["away_team"] == team) & (df["nmseason"] == s)]["fthg"].sum()
            number_of_games = len(df[((df["home_team"] == team) | (df["away_team"] == team)) & (df["nmseason"] == s)])
            if number_of_games != 0:
                rate = (goals_for - goals_against) / number_of_games
            else:
                rate = 0
            arr.append(rate)
        dict_res[team] = arr
    df2 = pd.DataFrame(dict_res, index=seasons_tableau, columns=teams)

    sns.set(style="ticks")

    df2[teams].plot()
    #return df2.to_html()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = img.getvalue()

    return Response(plot_url, mimetype='image/png')


@app.route("/get_positional_rating")

def get_positional_rating():
    conn = sqlite3.connect('data_app/seasons.db')

    home = request.values.get('team1')
    away = request.values.get('team2')
    df = pd.read_sql(
        sql='SELECT * from season WHERE home_team=? OR away_team=?  ORDER BY nmseason',
        con=conn, params=(home, away,))
    print(df[df.nmseason==11])
    seasons_tableau = df["nmseason"].unique()
    dict_res = {}
    teams = [home, away]

    dict_res1 = {}
    arr = []
    for s in seasons_tableau:
        goals_for = df[(df["home_team"] == home) & (df["nmseason"] == s)]["fthg"].sum()
        goals_against = df[(df["home_team"] == home) & (df["nmseason"] == s)]["ftag"].sum()
        number_of_games = len(df[(df["home_team"] == home) & (df["nmseason"] == s)])
        if number_of_games != 0:
            rate = (goals_for - goals_against) / number_of_games
        else:
            rate = 0
        arr.append(rate)
    dict_res1[home] = arr

    arr = []
    for s in seasons_tableau:
        goals_for = df[(df["away_team"] == away) & (df["nmseason"] == s)]["ftag"].sum()
        goals_against = df[(df["away_team"] == away) & (df["nmseason"] == s)]["fthg"].sum()
        number_of_games = len(df[(df["away_team"] == away) & (df["nmseason"] == s)])
        if number_of_games != 0:
            rate = (goals_for - goals_against) / number_of_games
        else:
            rate = 0
#print("For:{}, Against:{}, games:{}, seasom:{}, rate:{}".format(goals_for, goals_against, number_of_games, s,rate))
        arr.append(rate)
    dict_res1[away] = arr

    df3 = pd.DataFrame(dict_res1, index=seasons_tableau, columns=teams)
    print(df3)
    df3.plot()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = img.getvalue()

    return Response(plot_url, mimetype='image/png')


@app.route("/get_image")
def get_image():

    img = BytesIO()

    df1 = pd.read_csv('http://www.football-data.co.uk/mmz4281/1718/D1.csv', header=0, sep=',')


    plt.scatter(x=df1['FTAG'], y=df1['FTHG'], alpha=0.5)
    colors = np.random.rand(50)

    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = img.getvalue()
    # установить header conent-type  image/png

    return Response(plot_url, mimetype='image/png')

    #return plot_url.set_header('Content-Type', 'image/png')

#run the app
if __name__ == "__main__":
    app.run(debug=True)
