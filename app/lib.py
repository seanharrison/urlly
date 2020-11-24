import base64
import re
import secrets


def gen_id(num_bytes):
    """
    Generate a cryptographically random string id that can be used as a URL slug.

    * num_bytes = the number of cryptographically random bytes in the id string.

    The random id is encoded as a base64 string with the final '=' padding removed.
    Therefore, the returned id string is longer than num_bytes (as per the methods of
    base64). In other words, num_bytes is a measure of the size of pool of values from
    which the random string is generated, not a measure of the length of the result.
    """
    return (
        base64.urlsafe_b64encode(secrets.token_bytes(num_bytes)).rstrip(b'=').decode()
    )


def is_url(url):
    """
    Return True/False whether the given url is a url.

    We're using <https://mathiasbynens.be/demo/url-regex> and have selected the URL
    pattern by @diegoperini. With this pattern, false negative like
    'https://foo_bar.example.com/' are possible, but otherwise it's a good pattern.
    TODO: fix that without breaking anything else.
    """
    return bool(IS_URL_DIEGOPERINI.match(url))


# See <https://mathiasbynens.be/demo/url-regex> -- @diegoperini
IS_URL_DIEGOPERINI = re.compile(
    r'^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$',  # noqa
    re.I,
)
