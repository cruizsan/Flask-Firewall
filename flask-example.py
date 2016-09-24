from flask import Flask, request, abort
from security.firewall.flask_firewall import flask_firewall

app = Flask(__name__)

@app.before_request
def pre_request():
    # here log my user, get group for this user
    user_groups = ["IS_USER"]
    flask_firewall(request, user_groups, abort)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/api/test')
def api_test():
    return 'My API Test'

@app.route('/anonym/page')
def anonym_page():
    return 'My Anonymous Page'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
