from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
import schedule
import time
import pandas as pd
import numpy as np
import csv
from csv import reader
import os
import psycopg2

profile = True

create = input("Want to create a profile (y/n)?: ")
if create.lower() == "y":
  profile = True
elif create.lower() == "yes":
  profile = True
elif create.lower() == "ja":
  profile = True
else:
  profile = False
  user_username = input("Type username: ")

while profile == True:
  user_name = input("Type name: ")
  user_surname = input("Type surname: ")
  user_username = input("Type username: ")
  user_mail = input("Type e-mail: ")
  user_password = input("Type password: ")

  conn = psycopg2.connect(database="Scrape", user = "postgres", password="lennynico2011",host="localhost",port="5432")
  cur = conn.cursor()
  cur.execute("INSERT INTO profile VALUES (%s, %s, %s, %s, %s)", (user_name,user_surname,user_mail,user_password,user_username))
  cur.execute("SELECT * FROM profile;")
  print(cur.fetchall())
  conn.commit()
  cur.close()
  conn.close()
  profile = False

artist_names = []

flag = True

add = input("Want to add an artist (y/n)?: ")
if add.lower() == "y":
  flag = True
elif add.lower() == "yes":
  flag = True
elif add.lower() == "ja":
  flag = True
else:
  flag = False

while flag == True:
    #artist = []
    artist_name = input("Enter artist name: ")
    #artist.append(artist_name)
    #artist.append(",")
    artist_names.append(artist_name)
    another = input("Want to look for another artist (y/n)?: ")
    if another.lower() == "y":
      flag = True
    elif another.lower() == "yes":
      flag = True
    elif another.lower() == "ja":
      flag = True
    else:
      flag = False


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


def scraper():
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.implicitly_wait(10)

    for i in artist_names:
        artist_link = i.replace(" ","-")
        driver.get(f"https://soundcloud.com/{artist_link}/tracks")
        track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
        print(f"{i}'s most recent track is: {track.text} \nFind the link attached:")
        track_name = track.text
        link = get_link(artist_link)
        print(link)

        conn = psycopg2.connect(database="Scrape", user = "postgres", password="lennynico2011",host="localhost",port="5432")
        cur = conn.cursor()
        cur.execute("INSERT INTO scrapes VALUES (%s, %s, %s, %s, %s)", ('soundcloud',i,track_name,'change_of_value',user_username))
        cur.execute("SELECT * FROM scrapes;")
        print(cur.fetchall())
        conn.commit()
        cur.close()
        conn.close()
    driver.close()


if add.lower() == "y":
  scraper()
elif add.lower() == "yes":
  scraper()
elif add.lower() == "ja":
  scraper()

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
              #print(f"{rows[0]} just uploaded {track.text}")
              # dataframe.replace(to_replace =rows[2],value = title,inplace = True)
    cur.close()
    conn.close()
    driver.close()


# def check():
#     dataframe = pd.read_csv("scrape/data/Scrape.csv",header=None)
#     driver = webdriver.Safari()
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#     for index,rows in dataframe.iterrows():
#           artist_link = rows[0].replace(" ","-")
#           driver.get(f"https://soundcloud.com/{artist_link}/tracks")
#           track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
#           if track.text != rows[1]:
#               title = track.text
#               message = f"New track by {rows[0]}"
#               command = f'''
#               osascript -e 'display notification "{message}" with title "{title}"'
#               '''
#               os.system(command)
#               #print(f"{rows[0]} just uploaded {track.text}")
#               dataframe.replace(to_replace =rows[1],
#                  value = track.text,
#                   inplace = True)
#           dataframe.to_csv('scrape/data/Scrape.csv', header=None, index = False)
#     driver.close()

    # with open('scrape/data/Scrape.csv', 'r') as read_obj, open('scrape/data/Scrape.csv', 'w') as outfile:
    #     csv_reader = reader(read_obj,delimiter=',')
    #     writer =  csv.writer(outfile)
    #     for row in csv_reader:
    #       if row[0].lower() == 'elton john':
    #           row[0] = 1
    #           writer.writerow(row)
    #       else:
    #           row[0] = 0
    #           writer.writerow(row)

#check()

        # for row in csv_reader:
        #   artist_link = row[0].replace(" ","-")
        #   driver.get(f"https://soundcloud.com/{artist_link}/tracks")
        #   track = driver.find_element_by_css_selector("#content > div > div.l-fluid-fixed > div.l-main.l-user-main.sc-border-light-right > div > div.userMain__content > div > ul > li:nth-child(1) > div > div > div.sound__content > div.sound__header > div > div > div.soundTitle__usernameTitleContainer > a > span")
        #   if track != row[1]:


# from csv import DictReader, DictWriter


# with open('infile.csv', 'r') as infile, open('outfile.csv', 'w') as outfile:
#     reader = DictReader(infile)
#     writer = DictWriter(outfile, fieldnames=reader.fieldnames)
#     writer.writeheader()
#     for row in reader:
#         if row['host_location'].capitalize() == 'London':
#             row['host_location'] = 1
#         else:
#             row['host_location'] = 0
#         writer.writerow(row)



# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

schedule.every().minute.at(":00").do(check)

while True:
    schedule.run_pending()
    time.sleep(1)
