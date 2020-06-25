import praw
import wget
import time
import os
import tweepy
import os
from os import environ

def import_hmmm_posts():

    reddit = praw.Reddit(client_id='UNGy8Mu2f2Dbow', client_secret='oEsiIndElimXPZoi-Isp1Kq9E-8', user_agent='hmmm_bot_python')

    hot_posts = reddit.subreddit('Hmmm').top("day", limit=10)
    top_image = ""

    for post in hot_posts:

        url_used = False
        textfile = open("urls.txt", "r")
        if post.url in textfile.read():
            url_used = True
            print(post.url + " has already been used")
        textfile.close()

        if url_used == False:
            image_filename = wget.download(post.url)
            print("Downloaded " + image_filename)
            top_image = image_filename
            appendfile = open("urls.txt", "a")
            appendfile.write(post.url+"\n")
            appendfile.close()
            break
    return top_image

def tweet(filename):
    consumer_key = environ['CONSUMER_KEY']
    consumer_secret = environ['CONSUMER_SECRET']
    access_token = environ['ACCESS_KEY']
    access_secret = environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    try:
        api.update_with_media(top_image)
        print("Tweeting " +filename)
    except:
        print("Error sending tweet")

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    if i >= 300:
        file = open(fname, "w")
        file.truncate(0)
        file.close()
        print(fname + " has been cleared")
    i += 1
    print("There are " + str(i) +" URL entries in " + fname)
    return i

while True:
    top_image = import_hmmm_posts()
    tweet(top_image)
    file_len("urls.txt")  # gets length of file, clears log if i >- x (CHANGE IN FUNCTION TO LIKE 400)
    time.sleep(60)
    try:
        os.remove(top_image)
    except:
        print("Couldn't remove " + top_image)





