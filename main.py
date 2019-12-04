from time import sleep
from flask import json, request, Flask
import os
print(os.uname()[1])
if (os.uname()[1] == 'raspberrypi'):
    import RPi.GPIO as GPIO

# pins
motorPin = 25
commitPin = 24
starPin = 23

def setup():
    if (os.uname()[1] == 'raspberrypi'):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorPin, GPIO.OUT)
        GPIO.setup(commitPin, GPIO.OUT)
        GPIO.setup(starPin, GPIO.OUT)

def firePushAction():
    print("Push Happened!")
    if (os.uname()[1] == 'raspberrypi'):
        GPIO.output(motorPin, GPIO.HIGH)
        GPIO.output(commitPin, GPIO.LOW)
        GPIO.output(starPin, GPIO.HIGH)
        sleep(10)
        GPIO.cleanup()

def fireStarAction():
    print("Star Happened!")
    if (os.uname()[1] == 'raspberrypi'):
        GPIO.output(starPin, GPIO.HIGH)
        GPIO.output(starPin, GPIO.LOW)
        GPIO.output(starPin, GPIO.HIGH)
        GPIO.output(starPin, GPIO.LOW)
        GPIO.output(starPin, GPIO.HIGH)
        GPIO.output(starPin, GPIO.LOW)

def handleJson(gitJson):
    if "pusher" in gitJson:
        firePushAction()
    elif "starred_at" in gitJson:
        fireStarAction()
    pass

def fireLocalCommit():
    print("Local Commit Happened!")
    if (os.uname()[1] == 'raspberrypi'):
        GPIO.output(commitPin, GPIO.HIGH)
        GPIO.output(commitPin, GPIO.LOW)
        GPIO.output(commitPin, GPIO.HIGH)
        GPIO.output(commitPin, GPIO.LOW)
        GPIO.output(commitPin, GPIO.HIGH)
        GPIO.output(commitPin, GPIO.LOW)

app = Flask(__name__)

@app.route('/')
def api_root():
    return "welcome"

@app.route('/local', methods=['POST'])
def local_commit():
    fireLocalCommit()
    return "OK"

@app.route('/github', methods=['POST'])
def github_message():
    if request.headers['Content-Type'] == 'application/json':
        # print(json.dumps(request.json, indent=4, sort_keys=True))
        handleJson(request.json)
        return json.dumps(request.json, indent=4, sort_keys=True)

if __name__ == "__main__":
    app.run(debug=True)
    setup()



