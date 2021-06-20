SELECT
    MAX(runtime),
    MIN(runtime)
  FROM
    movies
 WHERE
    runtime > 0;
     --3
SELECT
    COUNT(DISTINCT production_companies)
  FROM
    movies;
     -- 4
SELECT
    COUNT(*),
    production_companies
  FROM
    movies
 GROUP BY
    production_companies;
     --5
SELECT
    COUNT(*),
    nvl(length(production_companies) - length(replace(production_companies, '|', '')), 0)
  FROM
    movies
 GROUP BY
    nvl(length(production_companies) - length(replace(production_companies, '|', '')), 0);
     --6
SELECT
    AVG(rate)
  FROM
    movies
 WHERE
    cast LIKE '%Maggie Smith%';
    --7
SELECT
    production_companies,
    SUM(revenue)
  FROM
    movies
 GROUP BY
    production_companies
 ORDER BY
    SUM(revenue) DESC;
    --8


SELECT
    *
  FROM
    (
        SELECT
            ( revenue - budget ) AS profit,
            original_title
          FROM
            movies
    )
 ORDER BY
    profit ASC;
     --14a
SELECT
    *
  FROM
    (
        SELECT
            ( revenue - budget ) AS profit,
            original_title
          FROM
            movies
    )
 ORDER BY
    profit DESC;
     --14b

SELECT
    EXTRACT(YEAR FROM release_date) AS myyear,
    COUNT(*)
  FROM
    movies
 WHERE
    genres LIKE '%Drama%'
 GROUP BY
    EXTRACT(YEAR FROM release_date)
 ORDER BY
    EXTRACT(YEAR FROM release_date);
         --15
