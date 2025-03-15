import sqlite3

from flask import Flask, jsonify
from flask_cors import CORS

from database import create_db

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/projects', methods=['GET'])
def get_projects():
    return jsonify({
        'total': 1,
        'items': [
            {
                'name': 'My WordPress site',
                'type': 'WordPress',
                'url': 'javiercasares.com',
                'version': '6.2',
                'extra': 'PHP 5.6',
            },
        ]
    })


if __name__ == '__main__':
    conn = sqlite3.connect('/data/app.db')
    create_db(conn)

    app.run()
