from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


def test_root_redirects_to_static_index():
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details():
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    response = client.get("/activities")

    assert response.status_code == 200
    assert set(response.json()) == set(activities)
    assert all(set(activity) == expected_fields for activity in response.json().values())


def test_signup_adds_participant_to_activity():
    activity_name = "Photography Club"
    email = "new.student@mergington.edu"
    participants_before = len(activities[activity_name]["participants"])

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert activities[activity_name]["participants"][-1] == email
    assert len(activities[activity_name]["participants"]) == participants_before + 1


def test_signup_rejects_duplicate_participant():
    activity_name = "Photography Club"
    email = "duplicate.student@mergington.edu"
    activities[activity_name]["participants"].append(email)
    participants_before = activities[activity_name]["participants"].copy()

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }
    assert activities[activity_name]["participants"] == participants_before


def test_signup_rejects_unknown_activity():
    email = "new.student@mergington.edu"

    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_requires_email():
    response = client.post("/activities/Photography Club/signup")

    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]


def test_missing_email_does_not_change_participants():
    activity_name = "Photography Club"
    participants_before = activities[activity_name]["participants"].copy()

    response = client.post(f"/activities/{activity_name}/signup")

    assert response.status_code == 422
    assert activities[activity_name]["participants"] == participants_before
