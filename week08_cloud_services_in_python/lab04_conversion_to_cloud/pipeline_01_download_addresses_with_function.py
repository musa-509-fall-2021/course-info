"""
Extract Process #1

Download addresses data from the given web location. Save to a local file in a
folder named "data/". You will have to create the folder before you can add
files to it (you don't have to create the folder in Python ... but you can if
you want to: https://docs.python.org/3/library/os.html#os.mkdir)
"""

import datetime as dt
import requests
from google.cloud import storage

print('Downloading the addresses data...')
response = requests.get('https://storage.googleapis.com/mjumbewu_musa_509/lab04_pipelines_and_web_services/get_latest_addresses')

print('Saving addresses data to a file...')
bucket_name = 'mjumbewu_cloudservices'
blob_name = f'addresses_{dt.date.today()}.csv'

outfile_path = f'data/addresses_{dt.date.today()}.csv'
with open(outfile_path, mode='wb') as outfile:
    outfile.write(response.content)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

upload_blob(bucket_name, outfile_path, blob_name)

print('Done.')
