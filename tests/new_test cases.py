
def test_access_denied(client):
    client, mongo = client  # Get client and mongo from fixture
    # No session set (unauthorized)
    response = client.get('/admin_dashboard')
    # Ensure unauthorized access returns 403
    assert response.status_code == 403


def test_register_voter_duplicate(client):
    client, mongo = client  # Get client and mongo from fixture

    # Add a voter manually to simulate duplicate scenario
    mongo.db.voters.insert_one({
        "name": "John Doe",
        "cnic": "12345",
        "dob": "2000-01-01"
    })

    # Set session for admin user
    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}

    # Try registering the same voter again
    response = client.post('/register_voter', json={
        "name": "John Doe",
        "cnic": "12345",
        "dob": "2000-01-01"
    })
    print("Register response (duplicate):", response.json)

    # Assertions
    assert response.json['success'] == False
    assert response.json['message'] == "Voter already registered."

    # Cleanup
    mongo.db.voters.delete_one({"cnic": "12345"})



def test_register_voter_success(client):
    client, mongo = client  # Get client and mongo from fixture
    
    # Cleanup: Ensure the voter doesn't already exist
    mongo.db.voters.delete_one({"cnic": "12345"})

    # Set session for admin user
    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}

    # Register voter
    response = client.post('/register_voter', json={
        "name": "John Doe",
        "cnic": "12345",
        "dob": "2000-01-01"
    })
    print("Register response (valid case):", response.json)

    # Assertions
    assert response.json is not None, "Response should not be None"
    assert response.json['success'] == True
    assert response.json['message'] == "Voter registered successfully."

    # Ensure voter exists in database
    voter = mongo.db.voters.find_one({"cnic": "12345"})
    assert voter is not None
    assert voter['name'] == "John Doe"
    assert voter['dob'] == "2000-01-01"

    # Cleanup
    mongo.db.voters.delete_one({"cnic": "12345"})


def test_register_voter_unauthorized(client):
    client, mongo = client  # Get client and mongo from fixture

    # No session set (unauthorized)
    response = client.post('/register_voter', json={
        "name": "John Doe",
        "cnic": "1234567890123",
        "dob": "2000-01-01"
    })

    # Ensure unauthorized access returns 403
    assert response.status_code == 403

    # Check if the response is JSON and contains the expected message
    if response.is_json:
        response_json = response.get_json()
        assert response_json is not None
        assert 'success' in response_json
        assert response_json['success'] is False
        assert 'message' in response_json
        assert "Unauthorized access" in response_json['message']  # Adjust based on actual error message
    else:
        # If the response is not JSON, assert that it's a forbidden message
        assert "Access Denied" in response.data.decode()  # Adjust based on actual error message

def test_register_voter_invalid_data(client):
    client, mongo = client  # Get client and mongo from fixture

    # Set session for admin user
    with client.session_transaction() as sess:
        sess['user'] = {"id": "admin123", "role": "admin"}

    # Try registering a voter with invalid data
    response = client.post('/register_voter', json={
        "name": "John Doe",
        "cnic": "12345",
        "dob": "2000-01-01"
    })
    print("Register response (invalid data):", response.json)
