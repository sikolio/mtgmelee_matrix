from app import app
from flask import render_template, request
import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def getRoundPairings(round_id):
    ENDPOINT = "https://mtgmelee.com/Tournament/GetRoundPairings/" + \
        str(round_id)
    r = requests.post(url=ENDPOINT)
    response = r.json()
    return response


def getPhaseStandings(phase_id):
    ENDPOINT = "https://mtgmelee.com/Tournament/GetPhaseStandings/" + \
        str(phase_id)
    r = requests.post(url=ENDPOINT)
    response = r.json()
    return response


@app.route('/')
@app.route('/index')
def index():
    # tournament_url = "https://mtgmelee.com/Tournament/View/374"
    # min_number_matches = 10
    # tournament = int(tournament_url.split('/')[-1])
    # response = requests.get(tournament_url)
    # soup = BeautifulSoup(response.text, "html.parser")

    # rounds = []
    # phases = []

    # for button in soup.findAll('button'):
    #     if(len(button['class']) == 3):
    #         if(button['class'][2] == 'round-selector'):
    #             if(button.text[0:5] == 'Round'):
    #                 rounds.append(button['data-id'])
    #             else:
    #                 phases.append(button['data-id'])

    # standing = getPhaseStandings(phases[-1])
    # data_players = []
    # for row in standing:
    #     if(row['Decklist'] == None):
    #         data_players.append([row['Player'], "Unknown"])
    #     else:
    #         data_players.append([row['Player'], row['Decklist']])

    # columns = ['Player','Decklist']
    # df_players = pd.DataFrame(data_players, columns=columns)

    # data_rounds = []
    # columns_mu = df_players['Decklist'].unique().tolist()
    # data_mu = [[0]*len(columns_mu) for _ in range(len(columns_mu))]

    # for round_id in rounds:
    #     round_list = getRoundPairings(round_id)
    #     for row in round_list:
    #         try:
    #             if('awarded a bye' in row['Result']):
    #                 continue

    #             deck_player = df_players[df_players['Player'] == row['Player']]['Decklist'].values[0]
    #             deck_opponent = df_players[df_players['Player'] == row['Opponent']]['Decklist'].values[0]
    #             if(row['Player'] in row['Result']):
    #                 mu_i = columns_mu.index(deck_player)
    #                 mu_j = columns_mu.index(deck_opponent)
    #                 if not(mu_i == mu_j):
    #                     data_mu[mu_i][mu_j] = data_mu[mu_i][mu_j] + 1
    #             elif(row['Opponent'] in row['Result']):
    #                 mu_j = columns_mu.index(deck_player)
    #                 mu_i = columns_mu.index(deck_opponent)
    #                 if not(mu_i == mu_j):
    #                     data_mu[mu_i][mu_j] = data_mu[mu_i][mu_j] + 1
    #         except:
    #             continue

    # data_mu_array = np.array(data_mu)
    # mask = data_mu_array.sum(axis=1) + data_mu_array.sum(axis=0) >= min_number_matches
    # columns_mu_short = [i for j, i in enumerate(columns_mu) if j not in tuple(np.where(mask == False)[0])]
    # data_mu_array_short = np.delete(data_mu_array, np.where(mask == False), 0)
    # data_mu_array_short = np.delete(data_mu_array_short, np.where(mask == False), 1)

    # def getMatrix(data_mu):
    #     [m, n] = data_mu.shape
    #     matrix = [[0]*(n+2) for _ in range(m)]

    #     for i in range(0, data_mu.shape[0]):
    #         string1 = str(np.round(100 * sum(data_mu[i,:]) / (sum(data_mu[i,:]) + sum(data_mu[:,i])),1))+"%"
    #         string2 = str(np.round(sum(data_mu[i,:]) + sum(data_mu[:,i]).round(1),1))
    #         matrix[i][0] = columns_mu_short[i]
    #         matrix[i][1] = string1+" ("+string2+")"
    #         for j in range(0, n):
    #             if(data_mu[i,j] + data_mu[j,i] > 0):
    #                 string3 = str(np.round(100 * data_mu[i,j] / (data_mu[i,j] + data_mu[j,i]),1))+"%"
    #                 string4 = str(np.round(data_mu[i,j] + data_mu[j,i],1))
    #                 matrix[i][j+2] = string3+" ("+string4+")"
    #             else:

    #                 matrix[i][j+2] = None
    #     return matrix

    # matrix = getMatrix(data_mu_array_short)
    # table_columns = ['', 'Total'] + columns_mu_short
    matrix = []
    table_columns = []

    return render_template('index.html', title='Home', matrix=matrix, columns=table_columns)


@app.route("/query", methods=["POST"])
def query():
    if request.method == 'POST':
        tournament_url = request.form['tournament_url']
        min_number_matches = 10
        tournament = int(tournament_url.split('/')[-1])
        response = requests.get(tournament_url)
        soup = BeautifulSoup(response.text, "html.parser")

        rounds = []
        phases = []

        for button in soup.findAll('button'):
            if(len(button['class']) == 3):
                if(button['class'][2] == 'round-selector'):
                    if(button.text[0:5] == 'Round'):
                        rounds.append(button['data-id'])
                    else:
                        phases.append(button['data-id'])

        standing = getPhaseStandings(phases[-1])
        data_players = []
        for row in standing:
            if(row['Decklist'] == None):
                data_players.append([row['Player'], "Unknown"])
            else:
                data_players.append([row['Player'], row['Decklist']])

        columns = ['Player', 'Decklist']
        df_players = pd.DataFrame(data_players, columns=columns)

        data_rounds = []
        columns_mu = df_players['Decklist'].unique().tolist()
        data_mu = [[0]*len(columns_mu) for _ in range(len(columns_mu))]

        for round_id in rounds:
            round_list = getRoundPairings(round_id)
            for row in round_list:
                try:
                    if('awarded a bye' in row['Result']):
                        continue

                    deck_player = df_players[df_players['Player']
                                            == row['Player']]['Decklist'].values[0]
                    deck_opponent = df_players[df_players['Player']
                                            == row['Opponent']]['Decklist'].values[0]
                    if(row['Player'] in row['Result']):
                        mu_i = columns_mu.index(deck_player)
                        mu_j = columns_mu.index(deck_opponent)
                        if not(mu_i == mu_j):
                            data_mu[mu_i][mu_j] = data_mu[mu_i][mu_j] + 1
                    elif(row['Opponent'] in row['Result']):
                        mu_j = columns_mu.index(deck_player)
                        mu_i = columns_mu.index(deck_opponent)
                        if not(mu_i == mu_j):
                            data_mu[mu_i][mu_j] = data_mu[mu_i][mu_j] + 1
                except:
                    continue

        data_mu_array = np.array(data_mu)
        mask = data_mu_array.sum(
            axis=1) + data_mu_array.sum(axis=0) >= min_number_matches
        columns_mu_short = [i for j, i in enumerate(
            columns_mu) if j not in tuple(np.where(mask == False)[0])]
        data_mu_array_short = np.delete(data_mu_array, np.where(mask == False), 0)
        data_mu_array_short = np.delete(
            data_mu_array_short, np.where(mask == False), 1)

        def getMatrix(data_mu):
            [m, n] = data_mu.shape
            matrix = [[0]*(n+2) for _ in range(m)]

            for i in range(0, data_mu.shape[0]):
                string1 = str(np.round(
                    100 * sum(data_mu[i, :]) / (sum(data_mu[i, :]) + sum(data_mu[:, i])), 1))+"%"
                string2 = str(
                    np.round(sum(data_mu[i, :]) + sum(data_mu[:, i]).round(1), 1))
                matrix[i][0] = columns_mu_short[i]
                matrix[i][1] = string1+" ("+string2+")"
                for j in range(0, n):
                    if(data_mu[i, j] + data_mu[j, i] > 0):
                        string3 = str(
                            np.round(100 * data_mu[i, j] / (data_mu[i, j] + data_mu[j, i]), 1))+"%"
                        string4 = str(np.round(data_mu[i, j] + data_mu[j, i], 1))
                        matrix[i][j+2] = string3+" ("+string4+")"
                    else:

                        matrix[i][j+2] = None
            return matrix

        matrix = getMatrix(data_mu_array_short)
        table_columns = ['', 'Total'] + columns_mu_short

        return render_template('index.html', title='Home', matrix=matrix, columns=table_columns)

