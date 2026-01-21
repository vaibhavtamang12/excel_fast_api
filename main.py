from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles # Add this
from fastapi.responses import FileResponse # Add this
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

class Entry(BaseModel):
    name: str
    email: str
    message: str

# --- API Endpoints ---

@app.post("/add-data")
async def add_data(entry: Entry):
    try:
        # Change "MyProjectSheet" to your actual Google Sheet name
        sheet = client.open("Practice").sheet1
        sheet.append_row([entry.name, entry.email, entry.message])
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Serve the Frontend ---

# This serves your HTML file at the root URL (http://127.0.0.1:8000/)
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# This mounts the 'static' folder so the app can find images or extra CSS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)