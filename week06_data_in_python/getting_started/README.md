The **data/** folder should contain:
* a folder called **census_2010_sf1/** containing a Census Explorer export
* a folder called **Census_Block_groups_2010/** containing an unzipped block groups shapefile for Philadelphia
* a file named **phl_neighborhoods.geojson** containing the Azavea neighborhoods GeoJSON file

## Installing dependencies

```bash
poetry install
```

## Running the script

```bash
poetry run python load_data.py
```
