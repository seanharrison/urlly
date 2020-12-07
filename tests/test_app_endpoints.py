def test_get_url_ok(client):
    """
    When we know that a URL exists with a given id, GET on that url id returns a
    redirect to the target location.
    """
    # first we need to create a URL (TODO: Use pytest-asyncio to database directly.)
    data = {'target': 'http://example.com'}
    response = client.post('/api/urls', json=data)
    result = response.json()
    print(result)
    url_id = result['data']['url']['id']

    # now we try the short URL
    response = client.get(f'/{url_id}', allow_redirects=False)
    assert response.status_code == 301
    assert response.headers['location'] == data['target']


def test_get_url_404(client):
    """
    When a URL does not exist with a given id, GET on that url id returns 404.
    """
    response = client.get('/NOT-AN-ID')
    assert response.status_code == 404
