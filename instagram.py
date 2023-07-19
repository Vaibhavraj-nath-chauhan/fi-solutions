import requests
import os
import random
import boto3
import time
from dotenv import load_dotenv
load_dotenv()


#Setting up the s3 session

session = boto3.Session( aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
s3 = session.resource('s3')
my_bucket = s3.Bucket(os.getenv("S3_BUCKET"))
    
def captions():
    file=open("hashtags.txt","r")
    hash = " ".join(random.sample(file.read().replace("\n","").split(","),k=10))
    captions = "Please show your support by giving us a like and a follow. \n\n\n\n\n" +hash
    return captions

# Creating a container to upload the file
def container(video_url=''):
    graph_url = os.getenv("GRAPH_API_URL")
    url = graph_url + os.getenv("INSTAGRAM_ACCOUNT_ID") + '/media'
    param = dict()
    param['access_token'] = os.getenv("ACCESS_TOKEN")
    param['caption'] = captions()
    param['video_url'] = video_url
    param['media_type'] = 'VIDEO'
    param['thumb_offset'] = '10'
    response = requests.post(url, params=param)
    response = response.json()
    return response


# publishing the container 
def publish_container(creation_id = '',):
    graph_url = os.getenv("GRAPH_API_URL")
    url = graph_url + os.getenv("INSTAGRAM_ACCOUNT_ID") + '/media_publish'
    param = dict()
    param['access_token'] = os.getenv("ACCESS_TOKEN")
    param['creation_id'] = creation_id
    response = requests.post(url,params=param)
    response = response.json()
    return response



# Fetching the files from the s3 
num=0
for my_bucket_object in my_bucket.objects.all():
    if num > 1:
        break
    id = my_bucket_object.key
    video_url = os.getenv("S3_BUCKET_LINK")+id
    response = container(video_url)
    time.sleep(30)
    response = publish_container(creation_id=response["id"])
    
    # Deleting the object we publish on s3
    my_bucket.delete_objects(
        Delete={
                'Objects': [
                    {
                        'Key': id
                    },
                ]
            }
        
    )
    num +=1
