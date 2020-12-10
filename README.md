# urlly - Cloud-native URL shortener

## Getting Started 

### Install Locally

Clone the archive, open a terminal, switch to the urlly project directory, and build the
app with docker-compose:
```bash
$ docker-compose build
```

### Run Locally

The following environment variables need to exist in the environment (`direnv` is nice,
this is your `.envrc`):
```bash
# replace 'urlly' with whatever values you want
export STACK_NAME=urlly
export HOST_NAME=localhost
export SITE_URL=http://${HOST_NAME}
export POSTGRES_DB=${STACK_NAME}
export POSTGRES_USER=${STACK_NAME}
export POSTGRES_PASSWORD=${STACK_NAME}
```
Then you can bring up the application:
```bash
docker-compose up
```
And hit it at http://localhost.

### Run Tests
```bash
docker-compose run app ./runtests.sh
```

## Installation and Deployment
This application is currently developed for Debian 10, which is available at most cloud
hosting providers. 

On the system / virtualhost / VPS / EC2 instance that you will be deploying on, open a
shell terminal (such as bash) and type the following:
```bash
wget https://raw.githubusercontent.com/seanharrison/urlly/main/debian-up.sh
chmod +x debian-up.sh
./debian-up.sh
```
The `./debian-up.sh` command will install system requirements, clone and cd to a "urlly"
folder, and create a `.envrc` file with environment variables and secrets. Edit the
values there before deploying.

To finish deploying the application and redeploy new versions, follow the instructions
given when `./debian-up.sh` has completed successfully: See [DEPLOY.md](DEPLOY.md).

---

## Technical / Architectural Notes
(As a substitute for doing architectural decision records.)

### Services

* router - nginx with rate limit (recommended: 2 req/sec from a given client IP)
* app - starlette app running behind gunicorn with uvicorn worker
    * /api = the api: JSON only
    * / = the ui: server-rendered bootstrap w/VueJS
* db - postgres container with persistent volume

#### API
(All API routes are relative to `/api`)

* GET / = `{"status": 200, "message": "Go on, then, shorten a URL."}`
* POST /urls = create new short URL for the given url.
    * request body: `{"url": "..."}`
    * response body: 
        * created: `{"status": 201, "message": "..." "data": {"url": {...}}}`
        * not a URL: `{"status": 422, "message": "didn't look like a URL to me,
          sorry."}`
* GET /urls/[ID]
    * found: 200 `{"status": 200, "data": {"url": {...}}}`
    * not found: 404 `{"status": 404, "message": "not found"}`

#### UI

* Input box for URL. Button: "Shorten".
* List previously-created short URLs in reverse chronological order under the input box.
* Browser-local storage (via localforage) for previously-created short URLs.
* GET /[ID] = the whole point of this thing: 
    * If the URL ID exists, redirects (301 Moved Permanently) to the target URL.
    * Otherwise, returns 404 Not Found

### Auth [TODO]

* Login with Google any time.
* Once logged in, UI syncs browser-local created URLs to our account.

### Security [TODO]

At this point there is no auth, no session, and no cookies. So we don't have any need
for HTTPS (except for getting rid of the "insecure" flag in recent browsers). However,
when we do implement auth, we will need to implement HTTPS and the works.

### Random ID for URL Shortener

* Length: 
    * Bit.ly uses 7 characters, but I recall when they used 6. 
    * Micro QR codes can be 21 characters. Assuming 14 characters for a tiny domain +
      root path (https://krx.li/), that leaves 7 chars. Could be why Bit.ly is 7
      characters!
    * So we'll use 7 characters.

* Charset:
    * urlsafe base64 is a good choice. We could pare it down to remove `1l0O` but we
      don't have any indication that people are going to type these. Instead, they're
      going to be generated automatically in our Twitter clone.

* Random:
    * It would be easy but naïve just to randomly generate some characters. The problem
      is that the library random function might or might not be cryptographically
      random. If it's not, then any user of our application might be able to guess which
      ids were created if they know what method we used (such as reading the source
      code). There is no security in obscurity. So we need to find a truly random
      character generator.
    * Cryptographically strong random bytes generators: 
        * Python: `secrets.token_bytes(length)`
        * PostgreSQL: `gen_random_bytes(length)` (in the crypto module)

* Encoding:
    * We can't deliver random bytes in a URL. So instead, we're going to use base64 to
      encode the random bytes. If we strip off the final ==, that cuts our randomness
      from 7 characters to 5.
    * 64^5 = 2^30 = 1,073,741,824 possible values.
