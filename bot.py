import os
import time
import random
import spintax
import requests
import config
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
import datab1
import json
import re
from urllib.parse import parse_qs, urlparse
import csv


PROXY = "3.88.169.225:80"


api_key = "AIzaSyDacb2_5wFLEPOANAsqk6fS0Rosw8lH6qk"



def stop(n):
    time.sleep(randint(2, n))

# login bot===================================================================================================


def youtube_login(email, password):
    LogIn = 'https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    op = webdriver.ChromeOptions()
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--disable-gpu')
    op.add_argument("--disable-infobars")
    op.add_argument("--log-level=3")
    op.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=op, executable_path=CM().install())
    driver.execute_script("document.body.style.zoom='80%'")
    driver.get(LogIn)

    print("=============================================================================================================")
    print("Google Login")

    email_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
    email_field.send_keys(email)
    driver.find_element_by_id("identifierNext").click()
    stop(5)
    print("email - done")

    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable(find_pass_field))
    pass_field.send_keys(password)
    driver.find_element_by_id("passwordNext").click()
    stop(5)
    print("password - done")
    WebDriverWait(driver, 200).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    print("Successfully login")
    print("============================================================================================================")

    return driver


# comment bot===================================================================================================
def comment_page(driver, comment):
    time.sleep(2)
    time.sleep(1)
    
    actions = ActionChains(driver)
    actions.send_keys(Keys.SPACE).perform()

    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(1)
    comment_box = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#placeholder-area'))
    WebDriverWait(driver, 4).until(comment_box)
    comment_box1 = driver.find_element_by_css_selector('#placeholder-area')
    ActionChains(driver).move_to_element(
        comment_box1).click(comment_box1).perform()
    add_comment_onit = driver.find_element_by_css_selector(
        '#contenteditable-root')
    add_comment_onit.send_keys(comment)
    r = random.randint(1, 100)
    
    
    driver.find_element_by_css_selector('#submit-button').click()
    print("done")

    stop(5)


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

    
def gotolink(driver, link):
    time.sleep(5)
    driver.get(link)





def get_youtube_video_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v")
    if video_id:
        return video_id[0]
    else:
        return None


def get_channel_id(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['snippet']['channelId']
    return None
   

def get_channel_name_by_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['snippet']['title']
    return None

def get_youtube_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"


def getCommentsFromLink(youtube_id):
    channel_id = get_channel_id(youtube_id)
    name = get_channel_name_by_id(channel_id)
    comment = "Hi " + name + " Hope You are doing good, This message is just to tell you that you are doing an awsome job."
    return(comment)


# running bot------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("hello")
    k = len(config.email)
    driver =[]
    cd = 0
    for i in range(k):
        email = config.email[i]
        password = config.password[i]
        print(password)
        driver1 = youtube_login(email, password)
        driver.append(driver1)
    
    with open('data2.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0])
            cd = cd%k
            workingDriver = driver[cd]
            vidId = get_youtube_video_id(row[0])
            print(vidId)
            comment = getCommentsFromLink(vidId)
            print(comment)
            gotolink(workingDriver, row[0])
            comment_page(workingDriver, comment)
            cd = cd+1
            
    


    
    
