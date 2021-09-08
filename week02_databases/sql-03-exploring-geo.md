
* [Geometry vs Geography performance benchmarks](https://medium.com/coord/postgis-performance-showdown-geometry-vs-geography-ec99967da4f0)
* [PostGIS: When to use Geography Data type over Geometry data type](https://postgis.net/docs/manual-2.4/using_postgis_dbmanagement.html#PostGIS_GeographyVSGeometry)

Map all the stations with statuses:

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

Notice that this query only returns one row. That's because `ST_Collect` is an aggregate function. There are [a bunch of these](https://postgis.net/docs/PostGIS_Special_Functions_Index.html#PostGIS_Aggregate_Functions) that we can use with PostGIS.

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

## More aggregation

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
