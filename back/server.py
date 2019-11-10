from flask import Flask, jsonify, request, Response
import fetchemail
import callendar

app = Flask(__name__)

personState = False
personList = None
emailState = False
registerUser = ['jackson']

@app.route('/checkForPerson')
def checkForPerson():
    global personState
    global personList
    resp = jsonify({'person': personState,'data':personList})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200

@app.route('/updatePersonState',methods=['POST'])
def updateState():
    global personState
    global personList
    json = request.json
    # {'person': [['Jackson', 'contempt']]}
    print(json)
    if len(json['person'])>0:
        personState = True
        personList = json['person']
    else:
        personState = False
        personList = []
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

@app.route('/readEmail')
def readEmail():
    r=fetchemail.main()
    print(r)
    return jsonify(r)
    #return 'hello'

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
