
# Using Geo-data and Aggregations

* [Geometry vs Geography performance benchmarks](https://medium.com/coord/postgis-performance-showdown-geometry-vs-geography-ec99967da4f0)
* [PostGIS: When to use Geography Data type over Geometry data type](https://postgis.net/docs/manual-2.4/using_postgis_dbmanagement.html#PostGIS_GeographyVSGeometry)

Open the station statuses data set. Map all the stations with statuses:

```sql
select *
from indego_station_statuses
```

Go over to the **STYLE** tab to show stations of different sizes according to the number of `totaldocks` at the station.

We can use geographic functions to explore the data in other ways. For example we can show the convex hull of all the stations with this query:

```sql
with stations_shape as (
  select st_convexhull(st_collect(the_geom)) as the_geom
  from indego_station_statuses
)

SELECT
  1 as cartodb_id,
  the_geom,
  st_transform(the_geom, 3857) as the_geom_webmercator
FROM stations_shape
```

_We include an additional column called `the_geom_webmercator`. This is a column that Carto requires for all of its maps. They are working to get rid of it. [Read about it in the Carto docs](https://carto.com/help/working-with-data/tips-for-geospatial-analysis/#about-the_geom_webmercator)._

Notice that this query only returns one row. That's because `ST_Collect` is an aggregation function. There are [a bunch of these](https://postgis.net/docs/PostGIS_Special_Functions_Index.html#PostGIS_Aggregate_Functions) that we can use with PostGIS.

[PostGIS Aggregate Functions](https://postgis.net/docs/PostGIS_Special_Functions_Index.html#PostGIS_Aggregate_Functions)

Another aggregate function is `ST_MakeLine`, which we can use to draw a line from one station to the next:

```sql
with stations_line as (
  select st_makeline(the_geom) as the_geom
  from indego_station_statuses
)

SELECT
  1 as cartodb_id,
  the_geom,
  st_transform(the_geom, 3857) as the_geom_webmercator
FROM stations_line
```

Using `order by`, we can control how the line is drawn. Here they're ordered by `addresszipcode` (I know this is a weird place to put `order by`):

```sql
with stations_line as (
  select st_makeline(the_geom order by addresszipcode) as the_geom
  from indego_station_statuses
)

SELECT
  1 as cartodb_id,
  the_geom,
  st_transform(the_geom, 3857) as the_geom_webmercator
FROM stations_line
```

```sql
with stations_line as (
  select st_makeline(the_geom order by st_setsrid(st_point(-75.162, 39.925), 4326) <-> the_geom) as the_geom
  from indego_station_statuses
)

SELECT
  1 as cartodb_id,
  the_geom,
  st_transform(the_geom, 3857) as the_geom_webmercator
FROM stations_line
```

Neat trick: open up your browser console and run:

```javascript
navigator.geolocation.getCurrentPosition(
  pos => {
    console.log(`${pos.coords.longitude}, ${pos.coords.latitude}`)
  },
  err => {
    console.log(err)
  }
)
```

Then use the coordinates returned to re-run the ordered distance query above. Another useful tool for finding coordinates of place is [geojson.io](https://geojson.io/).

-----------

Ok, let's use aggregation functions to actually start trying to answer a relevant question. For example, say I wanted to know what the demand at each station during a quarter was.

Open one of the `indego_trips` datasets.

```sql
select *
from indego_trips_2021_q1
```

First, notice it doesn't have a `the_geom` or a `the_geom_webmercator` column (which we'll need if we want to map the data). However, it does have two latitude/longitude pairs:
* `start_lat`/`start_lon`
* `end_lat`/`end_lon`

We can use these to create geometries. Let's start with the `start_` coordinates.

```sql
select
  cartodb_id,
  st_makepoint(start_lon, start_lat) as the_geom,
  st_transform(st_setsrid(st_makepoint(start_lon, start_lat), 4326), 3857) as the_geom_webmercator,
  trip_id,
  duration,
  start_time,
  end_time,
  start_station,
  end_station,
  bike_id,
  plan_duration,
  trip_route_category,
  passholder_type,
  bike_type
from indego_trips_2021_q1
```

Make a map from that query. It doesn't look more interesting than the map of stations (_Why?_). But since we have so much more data for each point, a heat map may be appropriate. I normally hate heat maps (they're too often and too easily overused and misused), but in this case, what does the heat map communicate?

## More aggregation

_What do we need to know to measure demand (in a simple way)?_

```sql
select
  start_station,
  count(*) as number_of_trips started
from indego_trips_2021_q1
group by start_station
```

We can map this with by adding the columns that Carto needs (`cartodb_id`, `the_geom`, and `the_geom_webmercator`):

```sql
select
  start_station,
  st_makepoint(start_lon, start_lat) as the_geom,
  st_transform(st_setsrid(st_makepoint(start_lon, start_lat), 4326), 3857) as the_geom_webmercator,
  row_number() over () as cartodb_id,
  count(*) as number_of_trips_started
from indego_trips_2021_q1
group by 1, 2, 3
```

(the `row_number() over ()` bit is a [window function](https://www.postgresql.org/docs/current/functions-window.html); window functions are pretty cool, but for now we're just going to use one to create a sequential number column)

Now we can go over to the **Style** tab and vary our map markers based on the station demand. That's kinda useful.

## Fancy aggregation

Aggregation functions aren't just for geographic elements -- we use aggregates on other data types too. For example, here's a more advanced query where we group the stations into 10 clusters and summarize the bikeshare station capacity in each one of the clusters:

```sql
with clustered_stations as (
  select *, ST_ClusterKMeans(the_geom, 10) over () as cluster
  from indego_station_statuses
),

station_clusters as (
  select
    cluster,
    st_concavehull(st_collect(the_geom), 0.1) as the_geom,
    count(*) as totalstations,
    sum(totaldocks) as totaldocks,
    sum(bikesavailable) as bikesavailable,
    sum(docksavailable) as docksavailable
  from clustered_stations
  group by cluster
)

select
  *,
  row_number() over () as cartodb_id,
  st_transform(the_geom, 3857) as the_geom_webmercator
from station_clusters
```
