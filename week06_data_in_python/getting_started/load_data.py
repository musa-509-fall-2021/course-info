import os
import pandas as pd
import geopandas as gpd
import sqlalchemy as sqa

project_root_path = os.path.dirname(__file__)

census_pop_df = pd.read_csv(
    os.path.join(project_root_path, 'data/census_2010_sf1/'
                 'DECENNIALSF12010.P1_data_with_overlays_2021-09-09T131935.csv'),
    skiprows=1,
)

census_block_groups_gdf = gpd.read_file(
    os.path.join(project_root_path, 'data/Census_Block_Groups_2010/'
                 'Census_Block_Groups_2010.shp')
)

neighborhoods_gdf = gpd.read_file(
    os.path.join(project_root_path, 'data/phl_neighborhoods.geojson')
)

db_engine = sqa.create_engine(
    'postgresql://postgres:postgres@localhost:5432/musa_509_2021'
)

print('Loading the census population data...')
census_pop_df.to_sql('census_population', db_engine)

print('Loading the census block groups...')
census_block_groups_gdf.to_postgis('census_block_groups', db_engine)

print ('Loading the Philadelphia neighborhoods...')
neighborhoods_gdf.to_postgis('phl_neighborhoods', db_engine)
