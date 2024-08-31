from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .models import Note
from .security import authenticate_user
from .spell_check import check_spelling
import json
import logging

app = FastAPI()
security = HTTPBasic()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NOTES_FILE = "app/notes.json"


def load_notes():
    try:
        with open(NOTES_FILE, "r") as f:
            notes = json.load(f)
            logger.debug(f"Loaded notes: {notes}")
            return notes
    except FileNotFoundError:
        logger.warning("Notes file not found, returning empty list")
        return []
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from notes file, returning empty list")
        return []


def save_notes(notes):
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=4)
            logger.debug(f"Saved notes: {notes}")
    except Exception as e:
        logger.error(f"Error saving notes: {e}")


@app.post("/notes/")
def add_note(note: Note, credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not note.content:
        raise HTTPException(status_code=422, detail="Note content cannot be empty")
    
    note.content = check_spelling(note.content)
    notes = load_notes()
    notes.append(note.dict())
    save_notes(notes)
    return {"message": "Note added successfully"}


@app.get("/notes/")
def list_notes(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    notes = load_notes()
    user_notes = [note for note in notes if note["user_id"] == user["id"]]
    return user_notes
