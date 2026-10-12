from fastapi import FastAPI

#This library is designed to generate cryptographically strong random numbers.
import secrets

#The urllib.parse module is very useful since you can do alot with it, keep it in the back
# of your mind whenever you're doing something interesting with python. 
#urlencode : spoken "url encode" encodes a dictionary (hashmap) into a URL-encoded query string

#urllib.parse falls into two categories. URL parsing, and URL encoding, in this case
# we're just going to be using URL encoding.
"""
Ex. 

params = {"search": "python tutorials", "page": 2}
urlencode(params)
# Output: 'search=python+tutorials&page=2'

Takes variables and just ampersands them together. Why is this useful?

Its useful cuz you can use the urlencode to get rid of any webserver specific literature
ex. buying & selling this won't be good cuz theres an ampersand here. So urlencode will fix it into 
a percent. %26 or something like this. 
"""
from urllib.parse import urlencode

"""

RedirectResponse is imported directly from the fastapi.responses module

This module just basically serves to redirect users to a certain url.

Where the fastapi.responses module contains JSONResponses which have the default
response thats used by FastAPI

Ex. from fastapi.responses import JSONResponses

HTMLResponses 

Ex. from fastapi.responses import HTMLResponses


""" 
from fastapi.responses import RedirectResponse

#This is just the sandbox key from tiktok, just a string basically.
CLIENT_KEY = "aw5bxfl6pdbn6b6m"

#This is the redirect uri, which is the url that TikTok will send you back to after you approve
# or deny it access. Also just a string btw.

REDIRECT_URI = "https://your-current-tunnel.trycloudflare.com/callback"

#Think of FastAPI as a class
# Like in java
# FastAPI app = new FastAPI() 
# But python just doesn't use the new keyword
# app is just an instance of the FastAPI() class.
app = FastAPI()
#This is just saying that you need to connect the /callback to the function below.
@app.get("/callback")
def callback():
        #The message is the key and the value is whatever's being printed out.
        return {"message" : "Server is live!"}
#The @ makes this a decorator.
@app.get("/login")
def login():
    return None

@app.get("/easter-egg")
#The name of the function doesn't matter as long as its below the path.
def egg():
      return "You found an easter egg celebrate!"