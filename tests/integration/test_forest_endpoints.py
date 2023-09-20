from fastapi.testclient import TestClient
from http import HTTPStatus


def test_list_predict(client: TestClient, test_image: bytes):
    files = {
        'image': test_image,
    }
    response = client.post('/forest_tags/predict', files=files)

    assert response.status_code == HTTPStatus.OK

    predicted_tags = response.json()['tags']

    assert isinstance(predicted_tags, list)


def test_str_predict(client: TestClient, test_image: bytes):
    files = {
        'image': test_image,
    }
    response = client.post('/forest_tags/predict', files=files)

    assert response.status_code == HTTPStatus.OK

    predicted_tags = response.json()['tags']

    assert all([isinstance(item, str) for item in predicted_tags])


def test_predict_proba(client: TestClient, test_image: bytes):
    files = {
        'image': test_image,
    }
    response = client.post('/forest_tags/predict_proba', files=files)

    assert response.status_code == HTTPStatus.OK

    tags_dict = response.json()['tags_probs']

    for key, value in tags_dict.items():
        assert isinstance(key, str)
        assert 0.0 <= float(value) <= 1.0
