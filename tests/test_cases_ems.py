import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, format_response, login_required, admin_required
import pytest
from flask import session
from datetime import datetime
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from dateutil.parser import isoparse
from datetime import datetime

def clean_date_string(date_str):
    # Remove the weekday part (e.g., 'Thu, ') and ' GMT' suffix
    try:
        # Remove the weekday part by splitting the string at the comma and taking the second part
        date_str = date_str.split(', ')[1]  
        # Remove ' GMT' from the string to make it compatible with isoparse
        date_str = date_str.replace(' GMT', '')  
        # Add 'Z' at the end to indicate the UTC timezone
        date_str = f"{date_str}Z"  
        return isoparse(date_str)  # Parse the cleaned-up string into a datetime object
    except Exception as e:
        print(f"Error in cleaning date string: {e}")
        return None
    
# Create a fixture to initialize the Flask app and MongoDB
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config["MONGO_URI"] = "mongodb+srv://bsef21m009:DcVFS1Pa0TaS3aFV@cluster0.rwzex.mongodb.net/evote"
    app.config["MONGO_DBNAME"] = "test"  # Use the test database
    mongo = PyMongo(app)  # Initialize PyMongo here

    with app.test_client() as client:
        with app.app_context():
            yield client, mongo  # Pass both client and mongo to the tests

# UNIT TESTS
def test_format_response():
    with app.app_context():
        response = format_response(True, "Success")
        assert response.json == {"success": True, "message": "Success", "data": None}

def test_format_response_with_data():
    with app.app_context():
        response = format_response(True, "Success", data={"id": 1})
        assert response.json == {"success": True, "message": "Success", "data": {"id": 1}}

def test_login_required_decorator():
    def mock_protected_route():
        return "Protected"
    decorated = login_required(mock_protected_route)
    with app.test_request_context():
        session['user'] = {"id": "test_user", "role": "voter"}
        result = decorated()
    assert result == "Protected"

def test_admin_required_decorator():
    def mock_protected_route():
        return "Admin Protected"
    decorated = admin_required(mock_protected_route)
    with app.test_request_context():
        session['user'] = {"id": "test_admin", "role": "admin"}
        result = decorated()
    assert result == "Admin Protected"

# INTEGRATION TESTS - Authentication
def test_login_voter(client):
    client, mongo = client  # Get client and mongo from fixture
    # Insert a test voter
    mongo.db.voters.insert_one({
        "name": "Marwa",
        "cnic": "987654321",
        "dob": "2000-07-07",
        "age": 34,
        "voted": False
    })
    response = client.post('/login', json={
        "cnic": "987654321",
        "dob": "2000-07-07"
    })
    print("Login response:", response.json)
    assert response.json['success'] == True
    mongo.db.voters.delete_one({"cnic": "987654321"})  # Clean up

def test_login_admin(client):
    client, mongo = client  # Get client and mongo from fixture
    # Insert a test admin
    mongo.db.admins.insert_one({
        "admin_id": "admin123",
        "name": "Admin User",
        "cnic": "99999",
        "dob": "1980-01-01"
    })
    response = client.post('/login', json={
        "cnic": "99999",
        "dob": "1980-01-01"
    })
    print("Admin login response:", response.json)
    assert response.json['success'] == True
    mongo.db.admins.delete_one({"cnic": "99999"})  # Clean up

# Voter Management
def test_register_voter(client):
    client, mongo = client  # Get client and mongo from fixture
    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}
    response = client.post('/register_voter', json={
        "name": "John Doe",
        # "cnic": "12345",
        "cnic": "11111",
        "dob": "2000-01-01"
    })
    print("Register response:", response.json)
    assert response.json['success'] == True
    mongo.db.voters.delete_one({"cnic": "11111"})  # Clean up

def test_add_candidate(client):
    client, mongo = client  # Get client and mongo from fixture

    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}


    # Add new candidate

    # Failed test:
    '''
    response = client.post('/add_candidate', json={
        "name": "alizay",
        "party": "A",
        "cnic": "67890",
        "dob": "1990-01-01"
    })
    '''
    response = client.post('/add_candidate', json={
        "name": "alizay",
        "party": "A",
        "cnic": "66666",
        "dob": "1990-01-01"
    })

    print("Add candidate response:", response.json)

    # Assert that the candidate is added successfully
    assert response.json['success'] == True

    # Clean up: remove candidate after the test
    mongo.db.candidates.delete_one({"cnic": "66666"})

def test_get_candidates(client):
    client, mongo = client  # Get client and mongo from fixture
    # Insert a test candidate
    candidate_id = mongo.db.candidates.insert_one({
        "name": "alizay",
        "party": "A",
        "cnic": "66666",
        "dob": "1990-01-01"
    }).inserted_id
    with client.session_transaction() as sess:
        sess['user'] = {"id": "voter123", "role": "voter"}
    response = client.get('/get_candidates')
    print("Get candidates response:", response.json)
    assert response.json['success'] == True
    mongo.db.candidates.delete_one({"_id": candidate_id})  # Clean up

# Election Management
def test_create_election(client):
    client, mongo = client  # Get client and mongo from fixture
    candidate_id = mongo.db.candidates.insert_one({
        "name": "alizay",
        "party": "A",
        "cnic": "55555",
        "dob": "1990-01-01"
    }).inserted_id

    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}

    # Clean up: Ensure no conflicting elections exist
    mongo.db.elections.delete_many({})

    # Clean up and convert the date to ISO 8601 format first
    start_date = clean_date_string("Thu, 12 Dec 2024 11:53:00 GMT")
    end_date = clean_date_string("Thu, 24 Dec 2024 01:54:00 GMT")

    response = client.post('/create_election', json={
        "name": "pti election",
        "start_date": start_date,  # Now passed as a datetime object
        "end_date": end_date,  # Now passed as a datetime object
        "candidate_ids": [str(candidate_id)]
    })
    print("Create election response:", response.json)
    assert response.json['success'] == True
    mongo.db.elections.delete_one({"name": "pti election"})  # Clean up
    mongo.db.candidates.delete_one({"_id": candidate_id})  # Clean up

def test_edit_election(client):
    client, mongo = client  # Get client and mongo from fixture

    # Insert a candidate
    candidate_id = mongo.db.candidates.insert_one({
        "name": "alizay",
        "party": "A",
        "cnic": "55555",
        "dob": "1990-01-01"
    }).inserted_id

    # Insert an election
    election_id = mongo.db.elections.insert_one({
        "name": "pti election",
        "start_date": clean_date_string("Thu, 12 Dec 2024 11:53:00 GMT"),
        "end_date": clean_date_string("Thu, 24 Dec 2024 01:54:00 GMT"),
        "candidates": [{"_id": candidate_id, "name": "alizay", "party": "A"}],
        "votes": {}
    }).inserted_id

    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}

    # Ensure the election exists before attempting to edit it
    election = mongo.db.elections.find_one({"_id": election_id})
    assert election is not None, "Election was not found in the database before edit."

    # Attempt to edit the election
    start_date = clean_date_string("Thu, 12 Dec 2024 11:53:00 GMT")
    end_date = clean_date_string("Thu, 24 Dec 2024 01:54:00 GMT")

    try:
        response = client.put(f'/edit_election/{str(election_id)}', json={
            "name": "updated election",
            "start_date": start_date,
            "end_date": end_date,
            "candidate_ids": [str(candidate_id)]
        })
        print("Edit election response:", response.json)

        # Assert that the response indicates success
        assert response.json['success'] == True
    finally:
        # Clean up the test data after assertions
        mongo.db.elections.delete_one({"_id": election_id})  # Delete the election
        mongo.db.candidates.delete_one({"_id": candidate_id})  # Clean up candidate
