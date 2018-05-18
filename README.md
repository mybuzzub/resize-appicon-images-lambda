resize-appicon-images-lambda function for AWS

Originally created by Sunil Joshi on 05/18/2018.

This Python based function triggers on an appicon (or launchimage) image file loaded into the source folder on an S3 bucket. It then creates images of different dimensions on a destination bucket on S3. These image dimensions are required for custom app submissions to the Apple App Store.

The main routine is in the .py file, while all the other folders contain the contents of the site-packages folder that got created when this Python program was originally setup on a linux machine with a virtualenv and various packages were pip-installed. Note that the boto3 package is not installed, as it comes bundled with AWS EC2 instances.