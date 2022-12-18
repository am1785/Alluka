import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '../.env'))
load_dotenv()

# generating random key for app
def main():
    print(os.urandom(24).hex())

class Config(object):
    # ...
    DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'soara.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'soara.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

if __name__ == '__main__':
    main()