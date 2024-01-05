import sys, dotenv, os, requests, json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from celery import Celery, Task
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from db import db, Device, Event, Command


load_dotenv()
token = os.getenv('AUTH_TOKEN')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

baseUrl = 'api.cloudpak.info'
UpdatesUrl = 'https://api.telegram.org/bot' + token + '/getUpdates'

SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')



def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db.init_app(app)
migrate = Migrate(app, db)

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)



@app.route('/')
def hello_world():
    return 'Hello. I am the CloudPak IoT bot.'

@app.route('/devices')
def devices():
    devices = Device.query.all()
    return render_template('devices.html', devices=devices)
@app.route('/events')
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)
@app.route('/commands')
def commands():
    commands = Command.query.all()
    return render_template('commands.html', commands=commands)

@app.route('/shelly')
def shelly():
    getShellyStatuses.delay()
    return 'Shelly statuses requested'

@app.route('/test', methods=['GET'])
def test():
    if request.method == 'GET':
        return render_template('test.html')
    else:
        return 'Nope'


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST' and request.headers['content-type'] == 'application/json':
            command = request.json['message']['text']
            chat_id = request.json['message']['chat']['id']
            type = request.json['message']['chat']['type']
            
            if type == 'private':
                if command == '/status':
                    # Get the connector statuses
                    connector_statuses = requests.get('https://' + baseUrl + '/api/v1/swithcs/status', 
                                                    headers={'Authorization': 'Bearer ' + token}).text
                    
                    # Send the statuses to the Telegram channel
                    requests.post('https://api.telegram.org/bot' + TELEGRAM_BOT_TOKEN + '/sendMessage', 
                                data={'chat_id': TELEGRAM_CHAT_ID, 'text': connector_statuses})
                    
                    return jsonify({"message": "Status sent to Telegram channel"}), 200

                if command == '/getstatus':
                    # Get the shelly statuses
                    getShellyStatuses.delay()
                    #return jsonify({"message": "Shelly statuses requested"}), 200
                    baseUrl='10.100.1.46'
                    statuses = requests.get('http://' + baseUrl + '/shelly/rpc', 
                                            params={"id":1, "method":"Mqtt.GetStatus"}).text
                    return jsonify({"message": "Test command " + statuses}), 200

                
                elif command == '/start':

                    return jsonify({"message": "Welcome to the CloudPak IoT bot"}), 200

            return jsonify(request.json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0:5030')