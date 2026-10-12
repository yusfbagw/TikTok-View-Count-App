from fastapi import FastAPI

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

@app.get("/")
#The name of the function doesn't matter as long as its below the path.
def bruh():
    return {"cool" : "Server is live right now"}