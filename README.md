# Overview

This repository is a step by step guid to finding the linear regression of TV shows bases on IMDB episode rating data.

# Steps

1. Download IMDB data [title.basics.tsv.gz, title.episode.tsv.gz, title.ratings.tsv.gz](https://datasets.imdbws.com/)
2. Extract and place into this repo
3. (Optional) run `tsv_to_csv.py` to convert files into `csv` (if you want to import data into SQL)
4. (Optional) import data into MySQL (I used DBeaver and it accepted csv files but did not like tsv files.I did still have to manually configure some column data times to strings to prevent conversation issues)
5. (Optional) Use slope.sql to create a view which calculates linear regression. This will create a view called `slopes`. Then you can run a query sun as this.

```sql
SELECT
	slopes.tconst,
	primaryTitle,
	startYear,
	round(slope,5) as slope,
	#slopes.totalVotes as totalEpisodeVotes,
	#slopes.runtimeMinutes,
	#title_ratings.numVotes as totalShowVotes,
	#slopes.averageRating as episodeAverageRating,
	title_ratings.averageRating as tvShowRating,
	episodeCount
FROM
	slopes
	INNER JOIN title_ratings on slopes.tconst = title_ratings.tconst
AND slopes.totalVotes > 50000
AND title_ratings.numVotes > 50000
AND episodeCount >= 30
ORDER by slope desc
```

6. Edit `imdb_ready.py` to include titles you're interested in.
7. Run `imdb_ready.py` to produce charts.
