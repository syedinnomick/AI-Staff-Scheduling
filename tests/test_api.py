import json
from backend.app import create_app

def test_health_and_flow():
    app = create_app()
    client = app.test_client()

    # create staff
    res = client.post("/api/staff", json={"name": "Alice", "role": "nurse", "specialty": "ICU"})
    assert res.status_code == 201
    staff_id = res.get_json()["id"]

    # list staff
    res = client.get("/api/staff")
    assert res.status_code == 200
    assert any(s["id"] == staff_id for s in res.get_json())

    # generate schedule
    res = client.post("/api/generate-schedule", json={"start_date": "2025-08-20", "days": 3})
    assert res.status_code == 201
    items = res.get_json()
    assert len(items) >= 2  # day+night per day

    # view schedule
    res = client.get("/api/view-schedule")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)
