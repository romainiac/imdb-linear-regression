alter VIEW Slopes as
SELECT 
  tconst,
  primaryTitle,
  startYear,
  slope,
  y_bar as averageRating,
  totalVotes,
  episodeCount
FROM
(
  SELECT 
    tconst,
    primaryTitle,
    startYear,
    y_bar,
    totalVotes,
    SUM((episodeCount - x_bar) * (averageRating - y_bar)) / SUM((episodeCount - x_bar) * (episodeCount - x_bar)) as slope,
    MAX(episodeCount) as episodeCount
  FROM
  (
    SELECT 
      tconst,
      primaryTitle,
      averageRating,
      totalVotes,
      startYear,
      AVG(averageRating) OVER (PARTITION BY primaryTitle, startYear) as y_bar,
      episodeCount,
      AVG(episodeCount) OVER (PARTITION BY primaryTitle, startYear) as x_bar
    FROM
    (
      SELECT 
      	tconst,
        primaryTitle,
        startYear,
        ROW_NUMBER() OVER (PARTITION BY primaryTitle,startYear ORDER BY seasonNumber, episodeNumber) AS episodeCount,
        averageRating,
        SUM(numVotes) OVER (PARTITION BY primaryTitle) as totalVotes
      FROM 
      (
        SELECT 
          tb.tconst,
          tb.primaryTitle,
          tb.startYear,
          tr.numVotes,
          CONVERT(te.seasonNumber, DECIMAL) as seasonNumber,
          CONVERT(te.episodeNumber, DECIMAL) as episodeNumber,
          tr.averageRating  
        FROM 
          title_basics as tb
          INNER JOIN title_episode as te on tb.tconst = te.parentTConst
          INNER JOIN title_ratings as tr on te.tconst = tr.tconst
        WHERE 
          tb.titleType = "tvSeries"
        ORDER BY 
          tb.tconst,primaryTitle, seasonNumber, episodeNumber, averageRating
      ) as a
    ) as b
  ) as c
  GROUP BY 
    tconst,primaryTitle, startYear, y_bar, totalVotes
) as d
WHERE slope IS NOT NULL;
ORDER by slope

SELECT 
	primaryTitle,
	startYear,
	slope,
	slopes.totalVotes as totalEpisodeVotes,
	title_ratings.numVotes as totalShowVotes,
	slopes.averageRating as episodeAverageRating,
	title_ratings.averageRating as tvShowRating,
	episodeCount
FROM 
	slopes 
	INNER JOIN title_ratings on slopes.tconst = title_ratings.tconst
WHERE slopes.averageRating > 7
AND title_ratings.averageRating > 7
AND slopes.totalVotes > 100000
AND episodeCount > 30
ORDER by slope desc















