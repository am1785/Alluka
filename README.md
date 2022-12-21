<p align="left">
  <img src="https://user-images.githubusercontent.com/25367083/208821632-aad4dc48-c30d-4e5c-91d8-b537c2c5fd1b.png" width="450" height="400"/>
  </p>

a lightweight English expressions search web application catered towards language learners built using flask, sqlite, JS, and data scoured from online videos (YouTube).

## Getting Started

### Install dependencies
> this repo requires `Python 3.7+` to be installed, and maybe having a new `venv` set up.

`pip install -r requirements.txt`

### Change `config.py` DB File Location
Line 14 -> `DATABASE = os.environ.get('DATABASE_URL') or \os.path.join(basedir, 'demo/soara.sqlite')`

### Initialize Database
from 1 level up the project root directory, run:
`flask --app Soara init-db`

### Run Flask App
`flask --app Soara --debug run`

the app should now be running locally on **http://127.0.0.1:5000**
