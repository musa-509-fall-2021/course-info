This walkthrough uses data downloaded from the [Indego Data](https://www.rideindego.com/about/data/) page, specifically:
* [Station Information (CSV)](https://www.rideindego.com/wp-content/uploads/2021/01/indego-stations-2021-01-01.csv) (link current as of Aug 31 2021)
* [Trip Data for Q1 2021 (Zipped CSV)](https://u626n26h74f16ig1p3pt0f2g-wpengine.netdna-ssl.com/wp-content/uploads/2021/04/indego-trips-2021-q1.zip) (link current as of Aug 31 2021; the Q2 data had a bug on that date, which is why I use the Q1 data below)
* [Real-time Station Status (GeoJSON)](https://kiosks.bicycletransit.workers.dev/phl) (should be different if you access it at different times.)

Download and unzip those files, and import into Carto as [new datasets](https://carto.com/help/tutorials/import-data-guide/).

```sql
select * from indego_stations
```

Notice that Carto "paginates" results, giving you 40 at a time.

Look through the `go_live_date` values. There are a few dates that have a number of stations going live.

Say we want to see all the stations that went live on a given date. You can filter based on equality.

```sql
select * from indego_stations
where go_live_date = '5/3/2016'
```

Now say we want to see all stations that went live _after_ a given date. You can also use inequalities to filter.

```sql
select * from indego_stations
where go_live_date > '5/3/2016'
```

This doesn't do what we expect because data types are important. Depending on the _type_ of data, we have different sets of operations to choose from, and those operations may behave differently.

[Complete list of _built-in_ PostgreSQL data types](https://www.postgresql.org/docs/current/datatype.html#DATATYPE-TABLE)

The `go_live_date` is stored as a `text` field. We can see this by running the following:

```sql
select "table_name", "column_name", "data_type"
from information_schema.columns
where table_name = 'indego_stations'
and column_name = 'go_live_date'
```
