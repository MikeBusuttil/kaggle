from os import environ
from time import strftime
from datetime import datetime, timedelta
from traceback import format_exc
from flask import Flask, request, jsonify
import db, log

app = Flask(__name__)

@app.route('/store', methods=['POST'])
def store():
    # ip_address = request.environ.get('HTTP_X_REAL_IP') or request.remote_addr
    try:
        assert(request.json['key'] == environ.get('AGENT_KEY'))
    except:
        log.stderr(request.json['key'] if request.is_json and 'key' in request.json else 'key error')
        log.stderr(environ.get('AGENT_KEY'))
        return jsonify({"msg": "unauthorized"}), 401

    try:
        assert('records' in request.json)
    except:
        return jsonify({"msg": "malformed request. Missing 'records' payload"}), 400

    try:
        db.store(request.json['records'])
    except:
        log.stderr(format_exc())
        return '👎', 500

    return '👍', 200

@app.route('/rmse', methods=['POST'])
def rmse():
    try:
        assert(request.json['key'] == environ.get('AGENT_KEY'))
    except:
        log.stderr(request.json['key'] if request.is_json and 'key' in request.json else 'key error')
        log.stderr(environ.get('AGENT_KEY'))
        return jsonify({"msg": "unauthorized"}), 401
    
    try:
        assert('filter' in request.json)
    except:
        return jsonify({"msg": "malformed request.  Missing 'filter' payload"}), 400

    try:
        return jsonify(db.rmse(request.json['filter'])), 200
    except:
        return '👎', 500

@app.route('/get', methods=['POST'])
def get():
    try:
        assert(request.json['key'] == environ.get('AGENT_KEY'))
    except:
        log.stderr(request.json['key'] if request.is_json and 'key' in request.json else 'key error')
        log.stderr(environ.get('AGENT_KEY'))
        return jsonify({"msg": "unauthorized"}), 401
    
    try:
        return jsonify({"records": db.get(request.json['filter'])}), 200
    except:
        return '👎', 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=False)
