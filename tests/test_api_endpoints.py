def test_home_get_ok(client):
    response = client.get('/api/')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 200


def test_urls_post_ok(client):
    data = {'target': 'http://example.com'}
    response = client.post('/api/urls', json=data)
    result = response.json()
    assert response.status_code == 201
    assert result['data']['url']['target'] == data['target']
    assert result['data']['url']['id']


def test_urls_post_not_json(client):
    data = ''
    response = client.post('/api/urls', data=data)
    assert response.status_code == 400


def test_urls_post_not_a_url(client):
    data = {'target': 'not-a-url'}
    response = client.post('/api/urls', json=data)
    assert response.status_code == 422


def test_url_get_ok(client):
    # first have to post a url
    data = {'target': 'http://example.com'}
    response = client.post('/api/urls', json=data)
    result = response.json()

    # now we can get that id
    url = '/api/urls/' + result['data']['url']['id']
    response = client.get(url)
    response_data = response.json()
    print(response_data)
    assert response.status_code == 200
    assert response_data['data']['url'] == result['data']['url']


def test_url_get_404(client):
    url = '/api/urls/not-an-id'
    response = client.get(url)
    assert response.status_code == 404
