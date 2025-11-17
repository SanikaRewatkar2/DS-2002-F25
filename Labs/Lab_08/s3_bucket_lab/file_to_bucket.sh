#!/bin/bash
set -e

# Take in positional arguments for  file, bucket, and timeout
# I'm going to prompt the user like I did in the pokemon lab
read -r -p "Enter Bucket Name: " BUCKET
read -r -p "Enter File Name: " FILE_NAME
read -r -p "Enter URL Timeout: " TIMEOUT

# First copy file to bucket
aws s3 cp $FILE_NAME s3://$BUCKET/
echo "-> $FILE_NAME copied to $BUCKET successfully!" >&2

# Then assemble url
aws s3 presign --expires-in  $TIMEOUT s3://$BUCKET/$FILE_NAME
echo "-> URL created successfully for $FILE_NAME!" >&2

