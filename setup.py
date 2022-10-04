import os, json, re
from setuptools import setup, find_packages
from codecs import open

PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PATH, 'README.md'), encoding='utf-8') as f:
    README = f.read()

if __name__ == '__main__':
    setup(
        name="urlly",
        version="0.1.0-alpha",
        description="Shorten urls",
        long_description=README,
        long_description_content_type='text/markdown',
        url="https://github.com/seanharrison/urlly",
        author="Sean Harrison",
        author_email="sah@bookgenesis.com",
        license="MPL 2.0",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Programming Language :: Python :: 3",
        ],
        install_requires=[
            "aiofiles~=22.1.0",
            "alembic~=1.8.1",
            "asyncpg~=0.26.0",
            "databases~=0.4.3",
            "gunicorn~=20.1.0",
            "httptools~=0.5.0",
            "Jinja2~=2.11.3",
            "MarkupSafe~=2.0.1",
            "orjson~=3.8.0",
            "psycopg2-binary~=2.9.3",
            "pydantic~=1.10.2",
            "requests~=2.28.1",
            "SQLAlchemy~=1.3.24",
            "starlette~=0.21.0",
            "uvicorn~=0.18.3",
            "uvloop~=0.17.0",
        ],
        extras_require={
            "dev": [
                "black~=22.8.0",
                "ipython~=8.5.0",
                "isort~=5.10.1",
            ],
            "test": [
                "black~=22.8.0",
                "flake8~=5.0.4",
                "httpx~=0.23.0",
                "pytest~=7.1.3",
                "pytest-cov~=4.0.0",
            ],
        },
        entry_points={},
        packages=find_packages(),
        package_data={"": []},
        data_files=[],
        scripts=[],
    )
