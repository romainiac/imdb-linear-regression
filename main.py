import requests
import json
import matplotlib.pyplot as plt
import numpy as np

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhOTVkZjJhZjc1ODQzYWViMTRmNjQ5NTY5MTQzNTdhOCIsInN1YiI6IjY1ZTlmMWUzMzg5ZGExMDE4MGQ4MDZhMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tsAabiB3NT0wyP5Z_77P2Z0fKQSIqV80uEIaaxjXEEU"
}

def get_scores(id):
    

black_list_id = 46952
the_office_id = 2316
the_wire = 1438
the_100 = 48866
the_bear = 136315
breaking_bad = 1396
tv_id = breaking_bad
tv_url = "https://api.themoviedb.org/3/tv/{tv_id}?language=en-US".format(tv_id=tv_id)
tv_season_url = url = "https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}?language=en-US"


response = requests.get(tv_url, headers=headers)
response = json.loads(response.text)

number_of_episodes = response["number_of_episodes"]
number_of_seasons = response["number_of_seasons"]
name = response["name"]

episode_reviews = []
for number_of_seasons in range(1, number_of_seasons + 1):
    url = tv_season_url.format(series_id=tv_id, season_number=number_of_seasons)
    season = json.loads(requests.get(url, headers=headers).text)
    episodes = season["episodes"]
    for episode in episodes:
        vote_average = episode["vote_average"]
        episode_reviews.append(vote_average)

x_axis = [item for item in range(0, len(episode_reviews))]

x_values = np.array(x_axis)
y_values = np.array(episode_reviews)

# Calculate the coefficients of the linear regression line
coefficients = np.polyfit(x_values, y_values, 1)

# Generate the y values of the regression line using the coefficients
regression_line = np.polyval(coefficients, x_values)

# Plot the data points
plt.scatter(x_values, y_values, label='Data Points')

# Plot the linear regression line
plt.plot(x_values, regression_line, label='Linear Regression Line', color='red')

# Set labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Display the legend and the graph
plt.legend()

slope_text = f'{coefficients[0]:.5f}'
print(name + slope_text)
plt.text(2, 4.5, slope_text, fontsize=30, color='blue')

plt.title(name + ": " + slope_text)

plt.grid(True)
plt.show()


