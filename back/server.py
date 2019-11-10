from flask import Flask, jsonify, request, Response
app = Flask(__name__)

personState = False

@app.route('/checkForPerson')
def checkForPerson():
    global personState
    resp = jsonify({'person': personState})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200

@app.route('/updatePersonState')
def updateState():
    global personState
    state = request.args.get('person')
    if state == 'yes':
        personState = True
    else:
        personState = False
    return 'success'

if __name__ == '__main__':
    app.run()
