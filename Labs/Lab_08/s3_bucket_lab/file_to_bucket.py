# sources:
# https://scrapeops.io/python-web-scraping-playbook/python-how-to-download-images/#using-urllib

# Ok, it's time to gif to bucket
import boto3
import requests

# url for the cute picture of a fox (i love foxes so much)
cute_fox_url = "https://cdn.pixabay.com/photo/2016/10/21/14/46/fox-1758183_1280.jpg"
response = requests.get(cute_fox_url) # get the cute little fox
filename = "cute_fox.jpg"
# pull file from internet into local file (cute_fox.jpg)
#print(response.status_code)
if response.status_code == 200: # if all good
    #print("Cute fox picture found!")
    with open(filename, "wb") as file: # create file and open
        file.write(response.content)
        #print("Cute fox file created!")

# make my client
s3 = boto3.client('s3', region_name='us-east-1')

# upload cute fox to my bucket
bucket = 'ds2002-f25-bux8fj'

s3.upload_file(
    Filename=filename,
    Bucket=bucket,
    Key=filename # key is just the filename
)

# code for presigned url from lab
expires_in = 604800 # seven day expiration time
# now generate the presigned url
response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': filename},
    ExpiresIn=expires_in
)

print(response) # output fox pic (which is a link that lets you... download the fox pic???)