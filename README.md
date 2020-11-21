# urlly - Cloud-native URL shortener


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

* Implementations:
    * Python:
        ```python
        import secrets, base64
        def gen_id(length):
            blen = (length * 3) // 4  # base64 takes 4/3 bytes to encode
            return base64.urlsafe_b64encode(secrets.token_bytes(blen)).rstrip(b'=')
        ```
    * PostgreSQL:
        ```sql
        CREATE EXTENSION IF NOT EXISTS pgcrypto;
        CREATE OR REPLACE FUNCTION gen_id(length integer) returns varchar as $$
            select 
            rtrim(
                replace(
                    replace(
                        encode(
                            -- base64 takes 4/3 bytes to encode
                            gen_random_bytes((length * 3 / 4)::integer), 
                            'base64'), 
                        '+', '-'), 
                    '/', '_'), 
                '=') as result;
        $$ LANGUAGE SQL;
        ```
    * Creating the id in Python means saving a select (returning id) from the database.
    * Creating the id in PostgreSQL means not being bound to a particular application layer.

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

* router - nginx with rate limit (max 2 req/sec from a given client IP)
* app - starlette app running behind gunicorn with uvicorn worker
    * /api = the api: JSON only
    * / = the ui: server-rendered bootstrap w/VueJS
* db - postgres container with PVC

#### API

* POST / = create new short URL for the given url.
    * request body: {"url": "..."}
    * response body: 
        * created: {"status": 201, "message": "..." "data": {"url": "...", "id": "..."}}
        * not a URL: {"status": 422, "message": "didn't look like a URL to me, sorry."}
* GET / = {"status": 200, "message": "Welcome to krx.li"}
* GET /[ID]
    * found: 301 => target URL
    * not found: 404 {"status": 404, "message": "not found"}

#### UI

* Input box for URL. Button: "Shorten".
* List previously-created short URLs reverse chrono under the input box.
* Browser-local storage for previously-created short URLs.

#### Auth [TODO]

* Login with Google any time.
* Once logged in, UI syncs browser-local created URLs to our account.

### Deployment

* GKE
* GitHub Actions for CI/CD from master
