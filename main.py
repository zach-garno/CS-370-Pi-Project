import time
from flask import json, request, Flask
import os
from multiprocessing import Process

print(os.uname()[1])
if os.uname()[1] == 'raspberrypi':
    import RPi.GPIO as GPIO

# pins
motorPin = 25
commitPin = 24
starPin = 23
photoPint = 27
photoPinm = 17
isHatOn = False

server = None


def setup():
    if os.uname()[1] == 'raspberrypi':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorPin, GPIO.OUT)
        GPIO.setup(commitPin, GPIO.OUT)
        GPIO.setup(starPin, GPIO.OUT)


def firePushAction():
    print("Push Happened!")
    if os.uname()[1] == 'raspberrypi' and isHatOn is True:
        GPIO.output(motorPin, GPIO.HIGH)
        GPIO.output(commitPin, GPIO.LOW)
        GPIO.output(starPin, GPIO.HIGH)
        time.sleep(10)
        GPIO.cleanup()


def fireStarAction():
    print("Star Happened!")
    if os.uname()[1] == 'raspberrypi':
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
    if os.uname()[1] == 'raspberrypi':
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


def startServer():
    if server is not None:
        server.start()
        print("server started!")
    else:
        print("server does not exist!")


def stopServer():
    if server is not None:
        server.terminate()
        print("server stopped!")
    else:
        print("server does not exist!")


if __name__ == "__main__":
    server = Process(app.run(debug=True))
    setup()
    cap = 0.000001
    adj = 2.130620985
    i = 0
    t = 0

    while True:
        GPIO.setup(photoPinm, GPIO.OUT)
        GPIO.setup(photoPint, GPIO.OUT)
        GPIO.output(photoPinm, False)
        GPIO.output(photoPint, False)
        time.sleep(0.2)
        GPIO.setup(photoPinm, GPIO.IN)
        time.sleep(0.2)
        GPIO.output(photoPint, True)
        startTime = time.time()
        endTime = time.time()

        while (GPIO.input(photoPinm) == GPIO.LOW):
            endTime = time.time()
        measureResistance = endTime - startTime
        resistance = (measureResistance/cap)*adj
        i = i + 1
        t = t + resistance
        if i == 10:
            t = t / i
            if t > 0:
                isHatOn = True
            else:
                isHatOn = False
            i = 0
            t = 0
