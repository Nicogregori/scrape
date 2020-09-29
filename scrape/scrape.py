from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import urllib.request



def get_link():
    source = urllib.request.urlopen(f"https://soundcloud.com/{artist_name}/tracks").read()
    soup = BeautifulSoup(source, 'lxml')
    section = soup.section

    links = []

    for url in section.find_all('a'):
        track_links = (url.get('href'))
        links.append(track_links)
    link = links[0]
    return f"https://soundcloud.com{link}"



driver = webdriver.Safari()
driver.maximize_window()
driver.implicitly_wait(10)

# using selenium to scrape specific trackname
# driver.get("https://soundcloud.com/chaos-in-the-cbd/tracks")
# track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
# track.text

flag = True

while flag == True:
    # using selenium to scrape any artists newest track
    artist_name = input("Enter artist name: ")
    driver.get(f"https://soundcloud.com/{artist_name}/tracks")
    track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
    print(f"{artist_name}'s most recent track is: {track.text} \nFind the link attached:")
    link = get_link()
    print(link)
    another = input("Want to look for another artist (y/n)?: ")
    if another.lower() == "y":
      flag = True
    elif another.lower() == "yes":
      flag = True
    elif another.lower() == "ja":
      flag = True
    else:
      flag = False




