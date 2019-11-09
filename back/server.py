from flask import Flask
app = Flask(__name__)

app.route('/checkForPerson')
def checkForPerson():
    pass

if __name__ == '__main__':
    app.run()