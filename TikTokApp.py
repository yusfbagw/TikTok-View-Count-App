from fastapi import FastAPI, Request

#This library lets python interact with your operating system. 
import os
#This lets you hide your environment variables inside of a env file, with two methods from these here as well.
from dotenv import find_dotenv, load_dotenv

#This is me just using the dotenv_path to find the env path and then just loading that into the load_dotenv() method.
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

#This library is designed to generate cryptographically strong random numbers.
import secrets

#We use this to send a POST request from my Python server to the TikTok server, for the access token. 
import httpx
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

#Defining CLIENT_SECRET
#We need to have this defined before this POST request can run
#This is where my client secret was.

CLIENT_SECRET = os.getenv("CLIENT_SECRET")

#This is just the sandbox key from tiktok, just a string basically.
#This is where my client key was
CLIENT_KEY = os.getenv("CLIENT_KEY")


if (not CLIENT_KEY or not CLIENT_SECRET):
      raise RuntimeError("Client key or client secret not loaded properly. Check .env file")
#This is the redirect uri, which is the url that TikTok will send you back to after you approve
# or deny it access. Also just a string btw.

REDIRECT_URI = "https://scenic-import-laden-photographer.trycloudflare.com"

#Think of FastAPI as a class
# Like in java
# FastAPI app = new FastAPI() 
# But python just doesn't use the new keyword
# app is just an instance of the FastAPI() class.
app = FastAPI()
#This is just saying that you need to connect the /callback to the function below.

"""

Going to work on validating the callback while login testing is blocked.

When tiktok redirects back we need to recieve a couple things here.

We get the URL query parameters: code and state. We need the code and the state
after a successfull approval, or error information if the authorization fails.

We also need to handle the oauth_state cookie we set before leaving.


To access incoming parts of a request add Request to ur fastapi import
"""
@app.get("/callback")
#Here request is an object representing the incoming HTTP request. The : Request annotation tells FastAPI to provide that object
# whenever we call this function.
def callback(request : Request):

      #get returns None if the requested value is missing so this handles our error checking.
      """
        
      Okay so the returned state is going to return some callback code, which which contain an exact 
      code that will match a cookie.

      In the cookie, we see the oauth_state will match the state thats in the browser, and then if they equal each other
      we proceed.
        
      """
      #ex. something returned from the tiktok api /callback?code=xyz223&state=abc123
      returned_state = request.query_params.get("state")
        
      #ex. abc123
      saved_state = request.cookies.get("oauth_state")
      #We can just test this by setting returned_state = abc123 and saved_state = abc123.
      #and then just checking the logic

      #saved_state and #returned_state checks that the URL value isn't missing or empty or if the cookie value isn't missing/empty
      #We want to verify that this browser started a login attempt, and not just that two Python values are equal, thats 
      #why we don't just check if the returned_state == saved_state.
      if (not saved_state or not returned_state or returned_state != saved_state):
            return{"message" : "State is not verified"}

      #Now we handle what tiktok actually sends back.
      #A matching state only confirms whether or not the response matches the login attempt it doesn't say anything
      #about whether the user has denied access or not.
      
      #This error is basically just that we're checking if there was an error w/ the returned state and the saved state.
      error = request.query_params.get("error")
      #The code is just the temp auth code we exchange for an access token to that TikTok acc.
      code = request.query_params.get("code")
      
      #If theres an error stop
      if error:
            #you could return None here, but thats not really that clear.
            #return None
            
            #returning a message would look cleaner and be better.
            return {"message" : "TikTok authorization failed."}
      #If theres no authorization code stop
      elif code == None:
            return {"message" : "Missing authorization code."}
      #Otherwise we're ready for a token exchange.
      else:
            token_response = httpx.post(
               "https://open.tiktokapis.com/v2/oauth/token/",
            data={
                  "client_key": CLIENT_KEY,
                  #The only area which I don't really understand yet is this. 
                  #This is just the client_secret, which is what authenticates your application to tiktok. We have to
                  #keep this private on our server.
                  "client_secret": CLIENT_SECRET,
                  "code": code,
                  "grant_type": "authorization_code",
                  "redirect_uri": REDIRECT_URI,
            },
            timeout=10.0,   
      )

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
        #The authorization code comes back in the callback URL.
        "response_type": "code",
        #These just the scopes that we need 
        "scope" : "user.info.basic,video.list",
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
    
    response.set_cookie saves the value in the browser; request.cookies.get() reads it when the browser sends it
    back.
    """
    response.set_cookie(
          #This is the cookies name: oauth_state
          "oauth_state",
          #State is its value
          state,
          #All this other stuff is basically just for security.
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