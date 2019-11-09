from flask import Flask,jsonify
app = Flask(__name__)

@app.route('/checkForPerson')
def checkForPerson():
    response = {'person':'no'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()