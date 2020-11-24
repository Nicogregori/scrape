import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
from pyvirtualdisplay import Display
import schedule
import numpy as np
import csv
from csv import reader
import os
import psycopg2
from firebase import firebase
import json


firebase = firebase.FirebaseApplication('https://scrape-6f8b8.firebaseio.com/', None)
result = firebase.get('', '')

def get_link(link_name):
    source = urllib.request.urlopen(f"https://soundcloud.com/{link_name}/tracks").read()
    soup = BeautifulSoup(source, 'lxml')
    section = soup.section

    links = []

    for url in section.find_all('a'):
        track_links = (url.get('href'))
        links.append(track_links)
    link = links[0]
    return f"https://soundcloud.com{link}"

def scraperZZZ(artists):
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.implicitly_wait(100)

    for i in artists:
        artist_link = i.replace(" ","-")
        driver.get(f"https://soundcloud.com/{artist_link}/tracks")
        track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
        print(f"{i}'s most recent track is: {track.text} \nFind the link attached:")
        track_name = track.text
        link = get_link(artist_link)
        print(link)

        firebase.put(f'/{user}/{sites}/',f'{i}',f'{track_name}')
        print('Record Updated')

    driver.close()


def scraper(artists):
    for i in artists:
      artist_link = i.replace(" ","-")
      source = urllib.request.urlopen(f"https://soundcloud.com/{artist_link}/tracks").read()
      soup = BeautifulSoup(source, 'html.parser')
      results = soup.find_all("a", class_="", itemprop="url")
      track_name = results[1].text
      firebase.put(f'/{user}/{sites}/',f'{i}',f'{track_name}')
      print('Record Updated')


def check():
    conn = psycopg2.connect(database="Scrape", user = "postgres", password="lennynico2011",host="localhost",port="5432")
    cur = conn.cursor()
    dataframe = pd.read_sql_query("SELECT * FROM scrapes;", conn)
    cur.execute("DELETE FROM scrapes;")
    cur.execute("SELECT * FROM scrapes;")
    conn.commit()
    print(cur.fetchall())
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.implicitly_wait(10)
    for index,rows in dataframe.iterrows():
          artist_link = rows[1].replace(" ","-")
          driver.get(f"https://soundcloud.com/{artist_link}/tracks")
          track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
          title = track.text
          cur.execute("INSERT INTO scrapes VALUES (%s, %s, %s, %s, %s)", ('soundcloud',rows[1],title,'change_of_value',user_username))
          conn.commit()
          if track.text != rows[2]:
              message = f"New track by {rows[1]}"
              command = f'''
              osascript -e 'display notification "{message}" with title "{title}"'
              '''
              os.system(command)
    cur.close()
    conn.close()
    driver.close()


for user, values in result.items():
    artists = []
    for sites, values_2 in values.items():
        for artist, track in values_2.items():
            artists.append(artist)
        scraper(artists)


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

# schedule.every().minute.at(":00").do(check)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
