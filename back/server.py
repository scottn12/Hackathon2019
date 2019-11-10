from flask import Flask, jsonify, request, Response
import fetchemail
import callendar

app = Flask(__name__)

personState = False
personList = None
emailState = False
registerUser = ['jackson']
hasMsg = False
Msg = ''

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
    resp = jsonify({'email': r})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200

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
        return jsonify(s)

@app.route('/confirmMsg',methods=['GET'])
def addComfirm():
    global hasMsg
    global Msg
    msg = request.args.get('msg')
    hasMsg = True
    Msg = msg
    return 'success'

@app.route('/checkMsg',methods=['GET'])
def ckMsg():
    global hasMsg
    if hasMsg:
        t = hasMsg
        hasMsg = False
        resp = jsonify({'status': t})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200
    else:
        resp = jsonify({'status': hasMsg})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200

@app.route('/getMsg',methods=['GET'])
def getMst():
    global Msg
    resp = jsonify({'msg': Msg})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 200

if __name__ == '__main__':
    app.run()
