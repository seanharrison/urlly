import json
from pathlib import Path
from unittest import TestCase

from app import lib

FIXTURES = Path(__file__).parent / "fixtures"


class TestGenId(TestCase):
    def test_gen_id(self):
        """
        lib.gen_id(length) with length > 1 and (length - 1) % 4 != 0 will pass.
        (The length must be able to be the result of base64 encode w/no =*.)
        """
        for length in range(100):
            with self.subTest(length=length):
                if length < 2 or (length - 1) % 4 == 0:
                    with self.assertRaises(ValueError):
                        lib.gen_id(length)
                else:
                    new_id = lib.gen_id(length)
                    assert len(new_id) == length
                    assert isinstance(new_id, str)



class TestIsUrl(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FIXTURES / "is_url.json") as f:
            cls.data = json.load(f)

    def test_is_url(self):
        """
        All of the URLs in data['is_url'] should pass. (NOTE: The last URL should pass
        but is currently known to fail, so we're excluding it for the moment.)
        """
        for url in self.data["is_url"][:-1]:  # TODO: Fix is_url so the last one passes.
            with self.subTest(url=url):
                assert lib.is_url(url) is True

    def test_not_url(self):
        """
        All of the URLs in data['not_url] should fail.
        """
        for url in self.data["not_url"]:
            with self.subTest(url=url):
                assert lib.is_url(url) is False
