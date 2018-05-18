from __future__ import print_function
import boto3
import os
import sys
import uuid
import PIL
from PIL import Image

# Created by Sunil Joshi on 05/18/2018.
#
# This Python based lambda function for AWS triggers on an appicon (or launchimage) image file loaded into the
# source folder on an S3 bucket. It then creates images of different dimensions on a destination bucket on S3.
# These image dimensions are required for custom app submissions to the Apple App Store.
# Note that boto3 is pre-installed on AWS EC2 instances

s3_client = boto3.client('s3')

appicon_dims = [
    "320x480",
    "640x960",
    "640x1136",
    "750x1334",
    "768x1004",
    "768x1024",
    "1024x748",
    "1024x768",
    "1125x2436",
    "1242x2208",
    "1536x2008",
    "1536x2048",
    "2048x1496",
    "2048x1536",
    "2208x1242",
    "2436x1125",
]

launchimage_dims = [
    "20x20",
    "29x29",
    "40x40",
    "58x58",
    "60x60",
    "76x76",
    "80x80",
    "87x87",
    "120x120",
    "152x152",
    "167x167",
    "180x180",
    "1024x1024"
]

def resize_image(image_path, resized_path, width, height):
    with Image.open(image_path) as image:
        newimg = image.resize((width, height), PIL.Image.ANTIALIAS)
        newimg.save(resized_path)

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print("New Event Triggered on bucket=" + bucket + ";ImageFile=", key)
        key_folder = key.split("/")[0]
        key_file = key.split("/")[1]
        key_file_base = key_file.split(".")[0]
        key_file_suffix = key_file.split(".")[1]
        download_path = '/tmp/{}{}{}'.format(uuid.uuid4(),key_folder,key_file)
        s3_client.download_file(bucket, key, download_path)

        selected_dims = []
        if key_folder == "appicon":
            selected_dims = appicon_dims
        elif key_folder == "launchimage":
            selected_dims = launchimage_dims

        for line in selected_dims:
            width = int(line.split('x')[0])
            height = int(line.split('x')[1])

            upload_path = '/tmp/resized-{}{}{}'.format(uuid.uuid4(),key_folder,key_file)
            resize_image(download_path, upload_path, width, height)
            newkey = key_folder + "/" + key_file_base + str(width) + "x" + str(height) + "." + key_file_suffix
            s3_client.upload_file(upload_path, '{}resized'.format(bucket), newkey)



