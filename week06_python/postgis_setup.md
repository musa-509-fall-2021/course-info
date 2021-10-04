# Getting PostGIS Setup

## Installing

### Windows

The PostGIS docs recommend [BostonGIS's guide to installing PostIGS](https://www.bostongis.com/PrinterFriendly.aspx?content_name=postgis_tut01#:~:text=Installing%20PostgreSQL%20with%20PostGIS%20Functionality) on Windows. It was written for PostgreSQL 9.5 and PostGIS 2.2, but should work for the latest versions as well. Generally speaking, those instructions are:

1. Download and install PostgreSQL from [EnterpriseDB](https://www.postgresql.org/download/windows/).
2. Run the “StackBuilder” utility and install the PostGIS add-on.

### Mac

Usually, [Postgres.app](https://postgresapp.com/) is the way to go. It's a pretty simple install. Just don't use `brew`.

## Connecting through a GUI

Once you have PostgreSQL installed, you should also have **pgAdmin**. You can use pgAdmin to create databases, and to run queries in a one-off way.

## Importing data from CSV files

The fastest way is with the `copy` SQL command ([docs](https://www.postgresql.org/docs/current/sql-copy.html)). Before running a `copy` command you have to create a table. For example

```sql
create table census_block_populations (
    "id" text,
    "name" text,
    "total" integer
);

copy census_block_populations
    from '/home/mjumbewu/Code/musa/musa-509/data/census_2010_sf1/DECENNIALSF12010.P1_data_with_overlays_2021-09-09T131935 (modified).csv'
    with (format csv, headers true);
```

Some things to note above:
* You must create the table to import into before running the `copy` command. There are tools to generate a SQL `create` statement by inferring from the contents of each column. For example, Pandas' [`to_sql`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html) will do this (and you might on a future homework too...).
* The field names in the database table do not have to match the field names in the CSV file, but the order of the fields _does_ have to match.
* You can be more explicit about which fields to load and in what order (which you might want to do if you have a bunch of fields in the CSV file that you don't care about), as below, but if you do then the field names _do_ have to match between the database table and the CSV file.

```sql
copy census_block_populations ("id", "name", "total")
    from '/home/mjumbewu/Code/musa/musa-509/data/census_2010_sf1/DECENNIALSF12010.P1_data_with_overlays_2021-09-09T131935 (modified).csv'
    with (format csv, headers true);
```

Alternatively, you could use tools in languages like R or Python (Pandas) to load data. Here's a Pandas snippet (adapted from [Ben's message to Slack](https://musa509610.slack.com/archives/C02CW5TGD7Y/p1633377338033500)):

```python
from sqlalchemy import create_engine
import pandas as pd

filepath = '/home/mjumbewu/Code/musa/musa-509/data/census_2010_sf1/DECENNIALSF12010.P1_data_with_overlays_2021-09-09T131935 (modified).csv'
table_name = 'census_block_populations'
pg_dbname = 'pg_getting_started'
pg_passwd = 'postgres'
pg_port = 5432

df = pd.read_csv(filepath)
# postgres doesn’t like capitals or spaces
df.columns = [c.lower() for c in df.columns]
engine = create_engine('postgresql://postgres:{pg_passwd}@localhost:{pg_port}/{pg_dbname}')
df.to_sql(table_name, engine)
```

## Importing data from Shapefiles

On Windows there is a GUI tool that comes with the EnterpriseDB installation of PostGIS to load shapefiles into a database. I do not know of such a GUI for Mac or Linux.

Two common command line tools to load Shapefile into Postgres are [`shp2pgsql`](https://postgis.net/docs/using_postgis_dbmanagement.html#shp2pgsql_usage) and [`ogr2ogr`](https://gdal.org/programs/ogr2ogr.html). I prefer to use the command line tool `ogr2ogr` because it also supports a number of other geospatial formats (though it doesn't do a great job of managing the complexity that comes with that flexibility). To use `ogr2ogr` to load a Shapefile into postgis you could use a command like:

```bash
sudo -u postgres \
    ogr2ogr \
    -f PostgreSQL PG:"host=localhost user=postgres dbname=pg_getting_started port=5432 password=postgres" \
    /home/mjumbewu/Code/musa/musa-509/data/Census_Block_Groups_2010/Census_Block_Groups_2010.shp \
    -nln census_block_groups
```

Just as there are alternatives for loading a CSV through Python, there are also alternatives for loading geospatial data using the GeoPandas library:

```python
from sqlalchemy import create_engine
import geopandas as gpd

filepath = '/home/mjumbewu/Code/musa/musa-509/data/Census_Block_Groups_2010-shp.zip!Census_Block_Groups_2010.shp'
table_name = 'census_block_populations'
pg_dbname = 'pg_getting_started'
pg_passwd = 'postgres'
pg_port = 5432

gdf = gpd.read_file(filepath)
engine = create_engine('postgresql://postgres:{pg_passwd}@localhost:{pg_port}/{pg_dbname}')
gdf.to_postgis(table_name, engine)
```
