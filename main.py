from fastapi import FastAPI, Request, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()

# Serve static files like CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_home():
    return FileResponse("frontend/index.html")

@app.get("/subscribe")
def get_subscribe():
    return FileResponse("frontend/subscribe.html")

@app.post("/api/search")
async def search(query: str = Form(...)):
    # You'd call your semantic MongoDB logic here
    return JSONResponse({
        "results": [
            "Deal 1 for " + query,
            "Deal 2 for " + query,
            "Deal 3 for " + query
        ]
    })

@app.post("/api/subscribe")
async def subscribe(email: str = Form(...)):
    # Send email to Brevo (hide API key in env)
    api_key = os.environ["BREVO_API_KEY"]
    response = requests.post(
        "https://api.brevo.com/v3/contacts",
        headers={
            "api-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "email": email,
            "listIds": [2]  # Replace with your Brevo list ID
        }
    )
    return JSONResponse(content=response.json())
