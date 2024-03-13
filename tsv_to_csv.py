import pandas

title_basics = pandas.read_csv('title.basics.tsv',sep='\t')
title_episodes = pandas.read_csv('title.episode.tsv',sep='\t')
title_ratings = pandas.read_csv('title.ratings.tsv',sep='\t')

title_basics.to_csv('title.basics.csv', sep=',')
title_episodes.to_csv('title.episode.csv', sep=',')
title_ratings.to_csv('title.ratings.csv', sep=',')