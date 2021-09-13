
Try these queries:

1. Date Parsing
  ```SQL
   SELECT to_timestamp('April 1, 2020',
                       'Month DD, YYYY')
   ```
2. Getting a timestamp type from a date and time
  ```SQL
  SELECT to_timestamp('2020/04/01 18:37:14',
                     'YYYY/MM/DD HH24:MI:SS')
  ```
3. Casting from a string:
  ```SQL
  SELECT '2020-09-08'::date
  ```
4. Parse a human readable date string to a date type:
  ```SQL
  SELECT to_date('08 Sep 2020', 'DD Mon YYYY')
  ```
5. Extracting part of a date:
  ```SQL
  SELECT
    EXTRACT(month from '2020-09-08'::date) as date_month,
    EXTRACT(day from '2020-09-08'::date) as date_day,
    EXTRACT(year from '2020-09-08'::date) as date_year
  ```

[PostgreSQL date/time documentation](https://www.postgresql.org/docs/12/datatype-datetime.html)

SQL Standard functions for:
* [`date` values](https://cloud.google.com/bigquery/docs/reference/standard-sql/date_functions)
* [`datetime` values](https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions)
* [`time` values](https://cloud.google.com/bigquery/docs/reference/standard-sql/time_functions)
* [`timestamp` values](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions)


## Returning to Carto...

We should now be able to filter all the stations added after a given date:

```sql
select * from indego_stations
where to_date(go_live_date, 'MM/DD/YYYY') > '2016-05-03'::date
```

To ensure that we don't have anything earlier than May 3, 2016, let's order by `go_live_date`:

```sql
select * from indego_stations
where to_date(go_live_date, 'MM/DD/YYYY') > '2016-05-03'::date
order by to_date(go_live_date, 'MM/DD/YYYY')
```

Pro-tip: we can use a common table expression (CTE) so that we don't have to specify the date parse code twice:

```sql
with transformed_indego_stations as (
  select *, to_date(go_live_date, 'MM/DD/YYYY') as parsed_go_live_date
  from indego_stations
)

select * from transformed_indego_stations
where parsed_go_live_date > '2016-05-03'::date
order by parsed_go_live_date
```
