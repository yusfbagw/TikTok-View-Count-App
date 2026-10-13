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
CLIENT_KEY = ""

#This is the redirect uri, which is the url that TikTok will send you back to after you approve
# or deny it access. Also just a string btw.

REDIRECT_URI = ""

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
    #This is going to create a random string for this login attempt.
    #We need this because our callback address is public, i.e (/callback)
    #We shouldn't accept a login response merely because it arrives there. 
    state = secrets.token_urlsafe(32)

    
    #This is just a dictionary full of the instructions that TikTok will need
    #The keys are the names that tiktok expects when you sent a request to it.
    #The values are what 
    parameters = {
        #The client key this is the application requesting access.
        "client_key": CLIENT_KEY,
        #Returns a temporary authorization code after approval
        #Sends a temp code to their email or whereever.
        "response_type": "code",
        #These just the scopes that we need 
        "scope" : "user.info.basic, video.list",
        #This is where we're going to redirect the user
        "redirect_uri" : REDIRECT_URI,
        #This state parameter is going to be the same random value when sending the browser back.
        "state" : state,
    }
    #Here we're building a destination URL. The part where the user would click on it and see an 
    # authorize or not page.
    url = "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(parameters)

    #This creates a HTTP response that tells the browser to go to this url, on the redirect.
    response = RedirectResponse(url)

    #This is a cookie
    """
    
    What we're doing here is basically we're creating a cookie.
    
    """
    response.set_cookie(
          #This is the cookies name: oauth_state
          "oauth_state",
          #State is its value
          state,
          #httponly prevents javascript running in the browser from accessing it through document.cookie.
          httponly=True,
          #Only sends the cookie over HTTPs, doesn't send it over an ordinary HTTP connection.
          secure=True,
          #This permits the cookie while restricting other cross site requests
          #Good for security. 
          samesite="lax",
          #max age in seconds
          max_age = 600
    )
    return response

@app.get("/easter-egg")
#The name of the function doesn't matter as long as its below the path.
def egg():
      return "You found an easter egg celebrate!"