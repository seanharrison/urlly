# urlly - Cloud-native URL shortener

## Getting Started 

### Install Locally
Use docker-compose:
```bash
docker-compose build
```

### Run Locally
The following environment variables need to exist in the environment (`direnv` is nice,
this is your `.envrc`):
```bash
# replace 'urlly' with whatever values you want
export POSTGRES_DB=urlly
export POSTGRES_USER=urlly
export POSTGRES_PASSWORD=urlly
```
Then you can bring up the API:
```bash
docker-compose up
```
And hit it at http://localhost:8000.

### Run Tests
```bash
docker-compose run app ./runtests.sh
```

## Deployment
Use any cloud-native provider to host postgresql and the app container / pod, inject POSTGRES_DB and DATABASE_URL into the app pod environment. There is currently no security, session, login, or rate-limiting. You can add auth and rate-limiting to an nginx ingress controller / router / reverse proxy.

### debian-up.sh
```bash
wget https://raw.githubusercontent.com/seanharrison/urlly/main/debian-up.sh
chmod +x debian-up.sh
./debian-up.sh
```

## Technical / Architectural Notes
(As a substitute for doing architectural decision records.)

### Random ID for URL Shortener

* Length: 
    * Bit.ly uses 7 characters, but I recall when they used 6. 
    * Micro QR codes can be 21 characters. Assuming 14 characters for a tiny domain + root path (https://krx.li/), that leaves 7 chars. Could be why Bit.ly is 7 characters!
    * So we'll use 7 characters.
    * Due to the birthday paradox, we'll want to revisit this decision if we get more than say 1% of the available values used up. 

* Charset:
    * urlsafe base64 is a good choice. We could pare it down to remove `1l0O` but we don't have any indication that people are going to type these. Instead, they're going to be generated automatically in our Twitter clone.

* Random:
    * It would be easy but naïve just to randomly generate some characters. The problem is that the library random function might or might not be cryptographically random. If it's not, then any user of our application might be able to guess which ids were created if they know what method we used (such as reading the source code). There is no security in obscurity. So we need to find a truly random character generator.
    * Cryptographically strong random bytes generators: 
        * Python: `secrets.token_bytes(length)`
        * PostgreSQL: `gen_random_bytes(length)` (in the crypto module)

* Encoding:
    * We can't deliver random bytes in a URL. So instead, we're going to use base64 to encode the random bytes. If we strip off the final ==, that cuts our randomness from 7 characters to 5.
    * 64^5 = 1,073,741,824 * 0.01 = 10,737,418. After we've made 10 million short URLs, we might want to do some more exploration.

### Not a URL?
```python
# <https://mathiasbynens.be/demo/url-regex>
import re
# is_url_stephenhay = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.I)
is_url_diegoperini = re.compile(r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$', re.I)

def is_url(url):
    """
    Must pass the diegoperini URL pattern - if positive, then it's a url.
    False negative like 'https://foo_bar.example.com/' are possible. TODO: fix that.
    """
    return bool(is_url_diegoperini.match(url))
```

### Services

* router [TODO] - nginx with rate limit (recommended    : 2 req/sec from a given client IP)
* app - starlette app running behind gunicorn with uvicorn worker
    * /api = the api: JSON only
    * / = the ui: server-rendered bootstrap w/VueJS
* db - postgres container with PVC

#### API
(All routes are relative to `/api`)

* GET / = `{"status": 200, "message": "Go on, then, shorten a URL."}`
* POST /urls = create new short URL for the given url.
    * request body: `{"url": "..."}`
    * response body: 
        * created: `{"status": 201, "message": "..." "data": {"url": {...}}}`
        * not a URL: `{"status": 422, "message": "didn't look like a URL to me, sorry."}`
* GET /urls/[ID]
    * found: 200 `{"status": 200, "data": {"url": {...}}}`
    * not found: 404 `{"status": 404, "message": "not found"}`

#### UI

* Input box for URL. Button: "Shorten".
* List previously-created short URLs reverse chrono under the input box.
* Browser-local storage (via localforage) for previously-created short URLs.

#### Auth [TODO]

* Login with Google any time.
* Once logged in, UI syncs browser-local created URLs to our account.
