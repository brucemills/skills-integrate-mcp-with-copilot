from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_requires_authentication():
    response = client.post('/activities/Chess Club/signup?email=test@example.com')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Authentication required'


def test_unregistered_student_cannot_manage_activities_without_authentication():
    response = client.delete('/activities/Chess Club/unregister?email=test@example.com')
    assert response.status_code == 401
    assert response.json()['detail'] == 'Authentication required'


def test_teacher_can_signup_students():
    response = client.post(
        '/activities/Chess Club/signup?email=test@example.com',
        headers={'Authorization': 'Bearer teacher-token'}
    )
    assert response.status_code == 200


def test_student_cannot_unregister_others():
    response = client.delete(
        '/activities/Chess Club/unregister?email=other@example.com',
        headers={'Authorization': 'Bearer student-token'}
    )
    assert response.status_code == 403
    assert response.json()['detail'] == 'Insufficient permissions'
