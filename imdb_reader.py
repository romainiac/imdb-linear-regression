import pandas
import numpy as np
import matplotlib.pyplot as plt

title_basics = pandas.read_csv('title.basics.tsv',sep='\t')
title_episodes = pandas.read_csv('title.episode.tsv',sep='\t')
title_ratings = pandas.read_csv('title.ratings.tsv',sep='\t')

# This matrix can be of any size (i hope). But i will limit it to 3x3 otherwise graphs will be too small
shows = [
        [("The Blacklist", "2013")]
         ]

figure, axis = plt.subplots(len(shows), len(shows[0])) 
figure.set_figwidth(15)
figure.set_figheight(10)

def search_tv_series(search, startYear):
    """
    Given a title (case sensitive) and a year, will return IMDB data for that title if found.
    Format of return is (list of episode numbers, list of episode ratings, title, startYear)
    """
    search_results = title_basics[(title_basics['primaryTitle'] == search) & (title_basics.startYear == startYear) & (title_basics['titleType'] == "tvSeries")]
    ratings = []
    title = ""
    if (len(search_results) > 0):
        tconst = search_results.iloc[0].tconst
        title = search_results.iloc[0].primaryTitle
        episodes = title_episodes[title_episodes['parentTconst'] == tconst]
        episodes = episodes[episodes['seasonNumber'] != "\\N"]
        episodes = episodes[episodes['episodeNumber'] != "\\N"]
        episodes['seasonNumber'] = episodes['seasonNumber'].astype(int)
        episodes['episodeNumber'] = episodes['episodeNumber'].astype(int)
        episodes = episodes.sort_values(by=['seasonNumber', 'episodeNumber'], ascending=[True, True])
        episode_ids = []
        for index, row in episodes.iterrows():        
            episode_ids.append(row.tconst)
        ratings = []
        for id in episode_ids:
            rating = title_ratings[title_ratings['tconst'] == id]
            if len(rating) > 0:
                ratings.append(rating.iloc[0]['averageRating'])

    x_axis = [item for item in range(1, len(ratings) + 1)]
    x_values = np.array(x_axis)
    y_values = np.array(ratings)
    return (x_values, y_values, title, startYear)


def plot(x_values, y_values, axisPos, title):
    coefficients = np.polyfit(x_values, y_values, 1)
    regression_line = np.polyval(coefficients, x_values)
    slope = coefficients[0]
    axisPos.set_title(title + ": " + "{:.4f}".format(slope), fontsize=25)
    axisPos.set_xlabel("Episode Number", fontsize=15)
    axisPos.set_ylabel("Episode Rating", fontsize=15)
    
    axisPos.scatter(x_values, y_values)
    axisPos.plot(x_values, regression_line, color='red')


# Loop through show matrix and plot graphs
for i in range(len(shows)):
    for j in range(len(shows[i])):
        name = search_tv_series(shows[i][j][0], shows[i][j][1])
        if len(shows) == 1 or len(shows[0]) == 1:
            plot(name[0], name[1], axis, name[2])
        else:
            plot(name[0], name[1], axis[i,j], name[2])


plt.grid(True)
plt.show()
