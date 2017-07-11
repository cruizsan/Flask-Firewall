from flask import Flask, request, jsonify
from security.firewall.flask_firewall import flask_firewall

app = Flask(__name__)


@app.before_request
def pre_request():
    # here log my user, get group for this user
    user_groups = ["IS_USER"]
    flask_firewall(request, user_groups)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/test')
def api_test():
    return 'My API Test'


@app.route('/anonym/page')
def anonym_page():
    return 'My Anonymous Page'


@app.errorhandler(403)
def unauthorized(e):
    return jsonify(
        code=403,
        error="unauthorized"
    )


@app.errorhandler(404)
def not_found(e):
    return jsonify(
        code=404,
        error="not found"
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
