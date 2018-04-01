# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import googlemaps

# load data
tourney = pd.read_csv('NCAATourneyDetailedResults.csv').iloc[:,0:6]
gamecities = pd.read_csv('GameCities.csv')
teams = pd.read_csv('Teams.csv').iloc[:,0:2]
cities = pd.read_csv('Cities.csv')

# merge/join data frames
city_joined = gamecities.set_index('CityID').join(cities.set_index('CityID'))
tourney_joined1 = pd.merge(tourney, teams, left_on='WTeamID', right_on='TeamID')
teams['LTeamID'] = teams['TeamID']
tourney_joined2 = pd.merge(tourney_joined1, teams, on='LTeamID')
data_final = pd.merge(city_joined, tourney_joined2, on=['Season', 'DayNum', 'WTeamID', 'LTeamID'])

# generate connection
gmaps = googlemaps.Client(key='AIzaSyBKPaH_-t3prNuJUTbcnklr1ePPn6oO71U')

# initialize lists
win_distances = [0]*len(data_final['WTeamID'])
loss_distances = [0]*len(data_final['WTeamID'])

# use api to get distances of winning and losing teams
for i in range(len(data_final['City'])):
    dest = data_final['City'].iloc[i]
    win_orig = data_final['TeamName_x'].iloc[i]
    loss_orig = data_final['TeamName_y'].iloc[i]
    if (gmaps.distance_matrix(win_orig, dest)['rows'][0]['elements'][0]['status'] == 'OK') and (gmaps.distance_matrix(loss_orig, dest)['rows'][0]['elements'][0]['status'] == 'OK'):
        distance1 = gmaps.distance_matrix(win_orig, dest)
        distance2 = gmaps.distance_matrix(loss_orig, dest)
        win_kilos = distance1['rows'][0]['elements'][0]['distance']['text']
        loss_kilos = distance2['rows'][0]['elements'][0]['distance']['text']
        win_distances[i] = float(win_kilos.split(' ')[0].replace(',', ''))
        loss_distances[i] = float(loss_kilos.split(' ')[0].replace(',', ''))
    else:
        win_distances[i] = 'NA'
        loss_distances[i] = 'NA'
        
# merge with data frame
data_final['winner_dist'] = win_distances
data_final['loser_dist'] = loss_distances

# remove NAs
data_final = data_final[data_final['winner_dist'] != 'NA']

# get distance advantage percentage
data_final['percent_advantage'] = (data_final['winner_dist'] - data_final['loser_dist'])/data_final['winner_dist']

# get distance advantage in kilometers
data_final['kilometer_advantage'] = data_final['loser_dist'] - data_final['winner_dist']
np.mean(data_final['kilometer_advantage'])
data_final.to_csv('home_advantage.csv')
