from flask import Flask, jsonify, request, Response
import callendar

app = Flask(__name__)

personState = False
emailState = False
registerUser = ['jackson']

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
# Rec
@app.route('/checkForEmail')
def checkForEmail():
    global emailState
    resp = jsonify({'email': emailState})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200

@app.route('/updateEmailState')
def updateEmailState():
    global emailState
    state = request.args.get('email')
    if state == 'yes':
        emailState = True
    else:
        emailState = False
    return 'success'

@app.route('/getSchedule')
def schedule():
    global registerUser
    person = request.args.get('user')
    if person not in registerUser:
        resp = jsonify({'status':'nRegistered'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200
    else:
        s = callendar.getSchedule(person)
        print(jsonify(s))
        return jsonify(s)
if __name__ == '__main__':
    app.run()
