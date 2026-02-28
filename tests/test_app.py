from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    # Arrange: nothing to set up beyond client and activities
    
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == set(activities.keys())


def test_signup_and_unregister_cycle():
    name = "Chess Club"
    email = "new@student.edu"

    # Arrange: ensure email not already in participants
    if email in activities[name]["participants"]:
        activities[name]["participants"].remove(email)

    # Act / Assert sequence
    resp = client.post(f"/activities/{name}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[name]["participants"]

    # duplicate signup should fail
    resp = client.post(f"/activities/{name}/signup?email={email}")
    assert resp.status_code == 400

    # unregister
    resp = client.delete(f"/activities/{name}/signup?email={email}")
    assert resp.status_code == 200
    assert email not in activities[name]["participants"]

    # removing again should return 404
    resp = client.delete(f"/activities/{name}/signup?email={email}")
    assert resp.status_code == 404


def test_nonexistent_activity():
    # Arrange/Act
    resp_post = client.post("/activities/Nope/signup?email=x@y")
    resp_delete = client.delete("/activities/Nope/signup?email=x@y")

    # Assert
    assert resp_post.status_code == 404
    assert resp_delete.status_code == 404
