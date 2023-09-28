import sys

from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'
@app.route('/menu')
def getData():

    return '{"{Command1":"Tetst"}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0:5030')