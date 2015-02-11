# EDT API

Ce projet a pour but de proposer une API facilement requêtable et présentant les données de http://emploidutemps.enpc.fr/.

[ ![Codeship Status for MickaelBergem/EDTAPI](https://codeship.com/projects/716d7300-5d3c-0132-0f32-76e6bb77e88f/status)](https://codeship.com/projects/51033)

## Installation

    git clone http://git.enpc.org/ki/emploidutemps-api.git emploidutemps-api && cd emploidutemps-api
    virtualenv --python=/usr/bin/python3 env
    source env/bin/activate

    pip install -r requirements.txt

## Usage

You can run `python scrapper.py` to retrieve the courses.

Run `python server.py` to run the server.
