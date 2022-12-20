# Soara
an English expressions search web application catered towards language learners built using flask, sqlite, reactJS, and data scoured from online videos (YouTube).

## Getting Started

### Install dependencies
> this repo requires `Python 3.7+` to be installed, and maybe having a new `venv` set up.

`pip install -r requirements.txt`

### Change Config.py DB File Location
Line 14 -> `DATABASE = os.environ.get('DATABASE_URL') or \os.path.join(basedir, 'demo/soara.sqlite')`

### Initialize Database
from 1 level up the project root directory, run:
`flask --app Soara init-db`

### Run Flask App
`flask --app Soara --debug run`

the app should now be running locally on **http://127.0.0.1:5000**
