import argparse
import json
import tempfile

import googleapiclient.discovery
import googleapiclient.http


def create_service():
    return googleapiclient.discovery.build('storage', 'v1')


def read_object(bucket, filename):
    with tempfile.TemporaryFile(mode='w+b') as tmpfile:
        get_object(bucket, filename, out_file=tmpfile)
        return tempfile


def get_object(bucket, filename, out_file):
    service = create_service()

    # Use get_media instead of get to get the actual contents of the object.
    # http://g.co/dv/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
    req = service.objects().get_media(bucket=bucket, object=filename)

    downloader = googleapiclient.http.MediaIoBaseDownload(out_file, req)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download {}%.".format(int(status.progress() * 100)))

    return out_file

