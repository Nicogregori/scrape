from firebase import firebase
import json
import requests



firebase = firebase.FirebaseApplication('https://scrape-6f8b8.firebaseio.com/', None)

result = firebase.get('', '')


# data = {...}
# result = firebase.post('/...', data)
# print(result)
