import pytest
import requests
import base64

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def auth_headers():
    credentials = "user1:password1"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    response = requests.get(f"{BASE_URL}/notes/", headers=headers)
    assert response.status_code == 200
    return headers

def test_add_note(auth_headers):
    note = {
        "id": 1,
        "user_id": 1,
        "content": "This is a test note"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Note added successfully"}

def test_list_notes(auth_headers):
    response = requests.get(f"{BASE_URL}/notes/", headers=auth_headers)
    assert response.status_code == 200
    notes = response.json()
    assert isinstance(notes, list)
    for note in notes:
        assert note["user_id"] == 1

def test_add_note_invalid_data(auth_headers):
    note = {
        "id": "invalid",
        "user_id": "invalid",
        "content": "This is a test note"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 422  # Unprocessable Entity

def test_add_note_no_authentication():
    note = {
        "id": 1,
        "user_id": 1,
        "content": "This is a test note"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note)
    assert response.status_code == 401  # Unauthorized

def test_add_note_wrong_credentials():
    credentials = "user1:wrongpassword"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    note = {
        "id": 1,
        "user_id": 1,
        "content": "This is a test note"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=headers)
    assert response.status_code == 401  # Unauthorized

def test_add_note_existing_id(auth_headers):
    note = {
        "id": 1,
        "user_id": 1,
        "content": "This is a test note"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 200  # Assuming it overwrites the existing note

def test_add_note_empty_content(auth_headers):
    note = {
        "id": 2,
        "user_id": 1,
        "content": ""
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 422  # Unprocessable Entity

def test_spell_check(auth_headers):
    note = {
        "id": 3,
        "user_id": 1,
        "content": "Ths is a tst nte"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Note added successfully"}

def test_add_note_very_long_content(auth_headers):
    long_content = "a" * 10000
    note = {
        "id": 4,
        "user_id": 1,
        "content": long_content
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Note added successfully"}

def test_add_note_nonexistent_user(auth_headers):
    note = {
        "id": 5,
        "user_id": 999,
        "content": "This is a test note"
    }
    response = requests.post(f"{BASE_URL}/notes/", json=note, headers=auth_headers)
    assert response.status_code == 200  # Assuming it allows notes for nonexistent users

def test_list_notes_nonexistent_user():
    credentials = "nonexistentuser:password"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    response = requests.get(f"{BASE_URL}/notes/", headers=headers)
    assert response.status_code == 401  # Unauthorized