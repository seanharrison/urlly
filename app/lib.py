import base64
import re
import secrets

# See <https://mathiasbynens.be/demo/url-regex> -- @diegoperini
IS_URL_DIEGOPERINI = re.compile(
    r"^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$",  # noqa
    re.I,
)


def gen_id(length):
    """
    Generate a cryptographically random string id that can be used as a URL slug, with
    the given length in the base64 character set.

    * Valid lengths: {2, 3, 4, 6, 7, 8, 10, 11, 12, ...}
    * Invalid lengths: {0, 1, 5, 9, 13, ...}

    Because of how we're doing this with base64, we can't create an id with length < 2
    or (length - 1) % 4 == 0. So raise a ValueError if one of those lengths is given.
    """
    if length < 2 or (length - 1) % 4 == 0:
        raise ValueError('Cannot create an id with length = %d' % length)

    # base64 takes 4/3 bytes to encode, so the random bytes are 3/4 length (as int).
    bytes_len = (length * 3) // 4
    return (
        base64.urlsafe_b64encode(secrets.token_bytes(bytes_len)).rstrip(b"=").decode()
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
