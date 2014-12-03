# EDT API

Ce projet a pour but de proposer une API facilement requêtable et présentant les données de http://emploidutemps.enpc.fr/.

## Installation

    git clone http://git.enpc.org/ki/emploidutemps-api.git emploidutemps-api
    cd emploidutemps-api
    virtualenv --python=/usr/bin/python3 env
    source env/bin/activate
    
    pip install -r requirements.txt
    
## Usage

You can run `python scrapper.py` to retrieve the courses.

Run `python server.py` to run the server.
