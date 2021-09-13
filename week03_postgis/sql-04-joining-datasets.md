# Joining Datasets

Let's say in addition to seeing the demand of the station we wanted to show information about the station when we click. We can do this in Carto with the **Popup** tab. However, right now all we have available is the station ID. We can use a join to get the station name.

```sql
select
  s.id,
  s.the_geom,
  s.the_geom_webmercator,
  s.cartodb_id,
  s.name,
  count(*) as number_of_trips_started
from indego_trips_2021_q1 t
join indego_station_statuses s on t.start_station = s.id
group by 1, 2, 3, 4, 5
```

Or we could refactor as:

```sql
with station_demand as (
  select
    start_station as id,
    count(*) as number_of_trips_started
  from indego_trips_2021_q1
  group by start_station
)

select
  s.cartodb_id,
  s.the_geom,
  s.the_geom_webmercator,
  s.id,
  s.name,
  d.number_of_trips_started
from station_demand d
join indego_station_statuses s on d.id = s.id
```

Now we can use the `name` field in the map popup.

## Joining on Geographic Fields

Let's say we wanted to know how many business there are in each neighborhood in the city.

We can get business license information from [Open Data Philly](https://opendataphilly.org/dataset/licenses-and-inspections-business-licenses). We can also get [neighborhood data](https://opendataphilly.org/dataset/philadelphia-neighborhoods).

We can load these into Carto and join across geographic columns.

```sql
with phl_business_licenses_by_neighborhood as (
  select
    n.name,
    count(*) as num_business_licenses
  from phl_business_licenses b
  join neighborhoods_philadelphia n
  on st_contains(n.the_geom, b.the_geom)
  group by n.name
)

select n.*, b.num_business_licenses
from phl_business_licenses_by_neighborhood b
join neighborhoods_philadelphia n
on n.name = b.name
```

_How would we normalize by the neighborhood size?_
