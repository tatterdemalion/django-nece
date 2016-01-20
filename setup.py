from setuptools import setup

with open('README.md', 'rb') as f:
    long_description = f.read().decode('utf-8')


setup(
    name='nece',
    version='0.1',
    description="A translation mechanism using Postgresql's "
                "jsonb field in the background",
    long_description=long_description,
    author='Can Mustafa Ozdemir',
    author_email='canmustafaozdemir@gmail.com',
    url='https://github.com/tatterdemalion/django-nece',
    download_url='https://github.com/tatterdemalion/django-nece/tarball/0.1',
    packages=['nece'],
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: Linguistic",
    ],
)
