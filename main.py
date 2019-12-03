from flask import json, request, Flask


def firePushAction():
    print("Push Happened!")

def fireStarAction():
    print("Star Happened!")

def handleJson(gitJson):
    if "pusher" in gitJson:
        firePushAction()
    elif "starred_at" in gitJson:
        fireStarAction()
    pass

def fireLocalCommit():
    print("Local Commit Happened!")

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



