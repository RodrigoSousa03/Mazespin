# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 19:14:08 2021

@author: User
"""

import tweepy
import cred
import time
from selenium import webdriver

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

while True:
    """
    selenium part - access mazespin website and get countup info
    """
    
    #global variables for selenium 
    DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
    URL = "https://mazesp.in/"
    #
    
    driver = webdriver.Chrome(DRIVER_PATH)
    
    driver.get(URL)
    
    try:
        search = driver.find_element_by_class_name("countup")
        time_spin = search.text
        print(time_spin)
        driver.quit()
    except:
        driver.quit()
        raise 
        
    """
    Twitter API part of the program
    """
    
    LAST_MENTION_FILE = "last_id.txt"
    LAST_WTF_FILE = "last_wtf.txt"
    LAST_F1_FILE = "last_f1.txt"
    
    
    auth = tweepy.OAuthHandler(cred.API_KEY, cred.API_SECRET_KEY)
    auth.set_access_token(cred.ACESS_TOKEN, cred.ACESS_TOKEN_SECRET)
    
    api = tweepy.API(auth)
    
    
    
    def write_id(last_tweet_id, filename):
        f1 = open(filename, "w")
        f1.write(str(last_tweet_id))
        f1.close()
        return
    
    def read_id(filename):
        f1 = open(filename, "r")
        last_tweet_id = int(f1.read().strip())
        f1.close()
        return last_tweet_id
        
    """tagged tweets"""
    tweets = api.mentions_timeline(read_id(LAST_MENTION_FILE), tweet_mode = "extended")
    
    for t in reversed(tweets):
        print(t.full_text)
        api.update_status("@" + t.user.screen_name + " It has been " + time_spin + " since our lord Mazespin last spun.", t.id )
        api.create_favorite(t.id)
    try:
        write_id(tweets[0].id, LAST_MENTION_FILE)
        print("Last tweet id stored.")
    except:
        print("No more tagged tweets. We are all up to date.")
        
    """tweets by wtf1"""
    tweets_wtf = api.user_timeline(since_id = read_id(LAST_WTF_FILE), screen_name = "@wtf1official", tweet_mode = "extended")
    
    for t in reversed(tweets_wtf):
        print(t.full_text)
        api.update_status("@" + t.user.screen_name + " Tag me to find out how long ago the one and only lord Mazespin last spun", t.id )
        api.create_favorite(t.id)
    try:
        write_id(tweets_wtf[0].id, LAST_WTF_FILE)
        print("Last tweet id stored.")
    except:
        print("No more tweets by wtf1. We are all up to date.")
        
    """tweets by f1"""
    tweets_f1 = api.user_timeline(since_id = read_id(LAST_F1_FILE), screen_name = "@F1", tweet_mode = "extended")
        
    for t in reversed(tweets_f1):
        print(t.full_text)
        api.update_status("@" + t.user.screen_name + " Tag me to find out how long ago the one and only lord Mazespin last spun", t.id )
        api.create_favorite(t.id)
    try:
        write_id(tweets_f1[0].id, LAST_F1_FILE)
        print("Last tweet id stored.")
    except:
        print("No more tweets by F1. We are all up to date.")
    
    print("end of program\n")
    time.sleep(300)
    