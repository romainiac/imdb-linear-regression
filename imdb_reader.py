import pandas
import numpy as np
import matplotlib.pyplot as plt

title_basics = pandas.read_csv('title.basics.tsv',sep='\t')
title_episodes = pandas.read_csv('title.episode.tsv',sep='\t')
title_ratings = pandas.read_csv('title.ratings.tsv',sep='\t')

#title_episodes.to_csv('title.episode.csv', sep=',')
#title_ratings.to_csv('title.ratings.csv', sep=',')


shows = [
        [("The Playboy Morning Show", "2010")]
         ]

figure, axis = plt.subplots(len(shows), len(shows[0])) 
figure.set_figwidth(15)
figure.set_figheight(10)

def search_tv_series(search, startYear):
    search_results = title_basics[(title_basics['primaryTitle'] == search) & (title_basics.startYear == startYear) & (title_basics['titleType'] == "tvSeries")]
    ratings = []
    if (len(search_results) > 0):
        tconst = search_results.iloc[0].tconst
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
    return ratings


def plot(x_values, y_values, axisPos, title):
    coefficients = np.polyfit(x_values, y_values, 1)
    regression_line = np.polyval(coefficients, x_values)
    slope = coefficients[0]
    axisPos.set_title(title + ": " + "{:.4f}".format(slope), fontsize=25)
    #axisPos.set_title(title, fontsize=25)
    axisPos.set_xlabel("Episode Number", fontsize=15)
    axisPos.set_ylabel("Episode Rating", fontsize=15)
    
    axisPos.scatter(x_values, y_values)
    axisPos.plot(x_values, regression_line, color='red')

def get_plot_data(search, year):
    ratings = search_tv_series(search, year)
    x_axis = [item for item in range(1, len(ratings) + 1)]
    x_values = np.array(x_axis)
    y_values = np.array(ratings)
    return (x_values, y_values, search, year)


for i in range(len(shows)):
    for j in range(len(shows[i])):
        name = get_plot_data(shows[i][j][0], shows[i][j][1])
        if len(shows) == 1 or len(shows[0]) == 1:
            plot(name[0], name[1], axis, name[2])
        else:
            plot(name[0], name[1], axis[i,j], name[2])

# breaking_bad = get_plot_data("Breaking Bad", "2008")
# the_wire = get_plot_data("The Wire", "2002")
# the_office = get_plot_data("The Office", "2005")
# print(len(the_office[0]))
# house = get_plot_data("House", "2004")
# suits = get_plot_data("Suits", "2011")
#the_blacklist = get_plot_data("The Blacklist", "2013")
# friends = get_plot_data("Friends", "1994")
# love_is_blind = get_plot_data("Love Is Blind", "2020")
# dancing = get_plot_data("Dancing with the Stars", "2005")
# square_off = get_plot_data("Square Off", "2006")
# early_show = get_plot_data("The Early Show", "1999")



# plot(breaking_bad[0], breaking_bad[1], axis[0,0], breaking_bad[2])
#plot(the_office[0], the_office[1], axis[0,1], the_office[2])
# plot(the_wire[0], the_wire[1], axis[1,0], the_wire[2])
# plot(house[0], house[1], axis[1,1], house[2])
# plot(suits[0], suits[1], axis[2,0], suits[2])
#plot(the_blacklist[0], the_blacklist[1], axis[2,1], the_blacklist[2])
#plot(dancing[0], dancing[1], axis[2,2], dancing[2])
#plot(square_off[0], square_off[1], axis[0,2], square_off[2])
#plot(early_show[0], early_show[1], axis[1,2], early_show[2])



plt.grid(True)
plt.show()
