import instaloader
import pandas as pd
import random
import os
import boto3
import shutil
from dotenv import load_dotenv
load_dotenv()


# Reading the csv file
data = pd.read_csv("status.csv", index_col=0)

# Fetching the page name and current number from the csv file and incrementing +3 
number = 3
page_name = random.choice(data['PAGE_NAME'].tolist())
post_number = data.loc[data['PAGE_NAME']==page_name, 'COUNT'].values[0]


# preparinng the loader 
Loader = instaloader.Instaloader()

# Fetching the post of the page
posts = instaloader.Profile.from_username(Loader.context, page_name).get_posts()

# Downloading the post 
num =0      
for post in posts:
    num +=1
    if num <= post_number:
        continue 
    if post.is_video:          
          Loader.download_post(post, "posts")
    else:
         num -=1
    if num == (post_number + number ):
        break
          
          
# Updating the post number in the file
data.loc[data['PAGE_NAME']==page_name, 'COUNT'] = data[data['PAGE_NAME']==page_name]['COUNT']+number
# Saving the file
data.to_csv("status.csv")



# setting up the s3 session to upload the file 
session = boto3.Session( aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
s3 = session.resource('s3')
my_bucket = s3.Bucket(os.getenv("S3_BUCKET"))
                
        
# Renaming the to upload the file to s3
num =max(list([int(my_bucket_object.key.split(".")[0]) for my_bucket_object in my_bucket.objects.all() ]))
for data in os.listdir("posts"):
    if ".mp4" in data:
        num +=1
        os.rename("posts/"+data, "posts/"+str(num)+".MP4") 
        my_bucket.upload_file("posts/"+str(num)+".MP4", str(num)+".MP4")
shutil.rmtree("posts")