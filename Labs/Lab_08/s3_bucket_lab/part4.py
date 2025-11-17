import boto3

# make my client
s3 = boto3.client('s3', region_name='us-east-1')

# make my request to list bucklets
response = s3.list_buckets()

# iterate through my response
for r in response['Buckets']:
    print(r['Name'])

# now let's upload the silly little flower picture to my bucket
bucket = 'ds2002-f25-bux8fj'
local_file = 'flowers.jpg'

# open it in binary read mode
with open(local_file, 'rb') as data:
    resp = s3.put_object(
        ACL= 'public-read', # make public
        Body=data,
        Bucket=bucket,
        Key=local_file
    )