from flask import Flask
app = Flask(__name__)

'''
Tutorial on venv

# Create a new virtualenv named "myproject"

$ virtualenv myproject

# Activate the virtualenv (OS X & Linux)
$ source myproject/Scripts/activate

# To deactive virtualenv
$ deactivate

'''

@app.route('/')
def hello_world():
   return 'Hello World'

if __name__ == '__main__':
   app.run(debug = True)