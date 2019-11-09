from flask import Flask,jsonify, request
app = Flask(__name__)

personState='no'

@app.route('/checkForPerson')
def checkForPerson():
    global personState
    response = {'person':personState}
    return jsonify(response)

@app.route('/updatePersonState')
def updateState():
    global personState
    state = request.args.get('person')
    personState = state
    return 'success'

if __name__ == '__main__':
    app.run()
