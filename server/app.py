import base64
import datetime
import os
import secrets

from cryptography.fernet import Fernet
from flask import Flask, jsonify, request, g, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, exceptions, verify_jwt_in_request, create_access_token
from dotenv import load_dotenv

from database import Database
from encryption import decrypt_message
from manifest import build_manifest


def create_app():
    app = Flask(__name__, static_folder='static/assets')
    app.config.from_object(__name__)

    JWTManager(app)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # Load environment variables from the .env file (if it exists)
    load_dotenv()

    env_defaults = {
        'DATABASE_PATH': 'app.db',
        'JWT_SECRET_KEY': lambda: secrets.token_hex(32),
        'JWT_ACCESS_TOKEN_EXPIRES': '120',
        'SECRET_KEY': lambda: base64.urlsafe_b64encode(Fernet.generate_key()).decode('utf-8'),
    }

    # Function to write the key-value pair to the .env file
    def write_to_env_file(key, value):
        with open('.env', 'a') as f:
            f.write(f"{key}={value}\n")
            print(f"Written {key} to .env file.")

    # Ensure all required environment variables are set
    for key, default in env_defaults.items():
        if not os.getenv(key):  # If the environment variable is not set
            value = default() if callable(default) else default
            os.environ[key] = value
            write_to_env_file(key, value)  # Store it in .env

    # Set the environment variables into Flask config
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=float(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH')
    app.config['SECRET_KEY'] = base64.urlsafe_b64decode(os.getenv('SECRET_KEY').encode('utf-8'))

    return app


# instantiate the app
app = create_app()
db_instance = Database(app.config['DATABASE_PATH'])


def is_static_path():
    return request.endpoint == 'index' or request.endpoint == 'static'


@app.before_request
def before_request():
    """Open the database connection before a request."""
    if not is_static_path():
        g.db = db_instance.get_connection()


@app.before_request
def check_route_exceptions():
    # Allow access to the login route without requiring JWT
    if is_static_path() or request.endpoint == 'ping' or request.endpoint == 'login':
        return  # Skip JWT required check for the login route

    try:
        verify_jwt_in_request()
    except exceptions.NoAuthorizationError:
        # Skip the jwt_required check for other routes, but raise the exception when needed
        return jsonify({"msg": "Missing authorization token"}), 401


@app.teardown_appcontext
def teardown(_):
    """Close the database connection after a request."""
    if hasattr(g, 'db'):
        db_instance.close_connection()


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/')
@app.route('/<path:path>')
@app.route('/<path:path>')
def index(path=None):
    return send_from_directory('static', 'index.html')


@app.route('/api/<path:path>')
def api_404(_):
    return jsonify({"error": "Route not found"}), 404


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = db_instance.get_user_by_login(
        data.get('email'),
        data.get('password')
    )

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user['email'], additional_claims={"user_id": user["id"]})
    return jsonify({"message": "Login successful", "user_id": user['id'], 'access_token': access_token}), 200


@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = db_instance.get_projects()

    return jsonify({
        'total': len(projects),
        'items': projects
    })


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = db_instance.get_project(project_id)

    provider = db_instance.get_provider(project['provider_id'])
    provider['apiKey'] = decrypt_message(provider['apiKey'])
    provider['apiSecret'] = decrypt_message(provider['apiSecret'])


    project['manifest'] = build_manifest(project, provider)

    return jsonify(project)


@app.route('/api/projects/<int:project_id>', methods=['POST'])
def update_project(project_id):
    data = request.get_json()

    try:
        db_instance.update_project(
            project_id,
            data.get('name'),
        )

        return jsonify({"message": f"Project updated successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/providers', methods=['GET'])
def get_providers():
    providers = db_instance.get_providers()

    return jsonify({
        'total': len(providers),
        'items': providers
    })


@app.route('/api/providers/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    provider = db_instance.get_provider(provider_id)
    provider['apiKey'] = decrypt_message(provider['apiKey'])
    provider['apiSecret'] = decrypt_message(provider['apiSecret'])

    return jsonify(provider)


@app.route('/api/providers/<int:provider_id>', methods=['POST'])
def update_provider(provider_id):
    data = request.get_json()

    try:
        db_instance.update_provider(
            provider_id,
            data.get('name'),
            data.get('type'),
            data.get('apiKey'),
            data.get('apiSecret'),
        )

        return jsonify({"message": f"Provider updated successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users', methods=['GET'])
def get_users():
    users = db_instance.get_users()

    return jsonify({
        'total': len(users),
        'items': users
    })


@app.route('/api/create-project', methods=['POST'])
def create_project():
    data = request.get_json()

    try:
        db_instance.add_project(
            data.get('name'),
            data.get('type'),
            data.get('provider_id'),
            data.get('instance'),
            data.get('url'),
            data.get('version', ''),
            data.get('extra', '')
        )

        return jsonify({"message": f"Project added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/add-provider', methods=['POST'])
def add_provider():
    data = request.get_json()

    try:
        db_instance.add_provider(
            data.get('name'),
            data.get('type'),
            data.get('api_key'),
            data.get('api_secret'),
        )

        return jsonify({"message": f"Provider added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/instances', methods=['POST'])
def get_instance_types():
    return jsonify({
        'regions': [
            'HEL1',
            'FSN1',
            'NBG1',
        ],
        'plans': [
            {
                'name': 'Shared vCPU Intel',
                'options': [
                    {
                        'name': 'CX22',
                        'VCPU': 2,
                        'RAM': 4,
                        'disk': 40,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0074,
                        'price_month': 4.59,
                    },
                    {
                        'name': 'CX32',
                        'VCPU': 4,
                        'RAM': 8,
                        'disk': 80,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0127,
                        'price_month': 7.59,
                    },
                    {
                        'name': 'CX42',
                        'VCPU': 8,
                        'RAM': 16,
                        'disk': 160,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0304,
                        'price_month': 18.59,
                    },
                    {
                        'name': 'CX52',
                        'VCPU': 16,
                        'RAM': 32,
                        'disk': 320,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0611,
                        'price_month': 36.09,
                    }
                ]
            },
            {
                'name': 'Shared vCPU AMD',
                'options': [
                    {
                        'name': 'CPX11',
                        'VCPU': 2,
                        'RAM': 2,
                        'disk': 40,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0082,
                        'price_month': 5.09,
                    },
                    {
                        'name': 'CPX21',
                        'VCPU': 3,
                        'RAM': 4,
                        'disk': 80,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0138,
                        'price_month': 8.59,
                    },
                    {
                        'name': 'CPX31',
                        'VCPU': 4,
                        'RAM': 8,
                        'disk': 160,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.025,
                        'price_month': 15.59,
                    },
                    {
                        'name': 'CPX41',
                        'VCPU': 8,
                        'RAM': 16,
                        'disk': 240,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0464,
                        'price_month': 28.09,
                    },
                    {
                        'name': 'CPX51',
                        'VCPU': 16,
                        'RAM': 32,
                        'disk': 360,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0979,
                        'price_month': 61.09,
                    }
                ]
            },
            {
                'name': 'Shared vCPU Ampere',
                'options': [
                    {
                        'name': 'CAX11',
                        'VCPU': 2,
                        'RAM': 4,
                        'disk': 40,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0074,
                        'price_month': 4.59,
                    },
                    {
                        'name': 'CAX21',
                        'VCPU': 4,
                        'RAM': 8,
                        'disk': 80,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0122,
                        'price_month': 7.59,
                    },
                    {
                        'name': 'CAX31',
                        'VCPU': 8,
                        'RAM': 16,
                        'disk': 160,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0226,
                        'price_month': 14.09,
                    },
                    {
                        'name': 'CAX41',
                        'VCPU': 16,
                        'RAM': 32,
                        'disk': 320,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0443,
                        'price_month': 27.59,
                    }
                ]
            },
            {
                'name': 'Dedicated vCPU',
                'options': [
                    {
                        'name': 'CCX13',
                        'VCPU': 2,
                        'RAM': 8,
                        'disk': 80,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0226,
                        'price_month': 14.09,
                    },
                    {
                        'name': 'CCX23',
                        'VCPU': 4,
                        'RAM': 16,
                        'disk': 160,
                        'disk_type': 'NVME SSD',
                        'traffic': 20,
                        'price_hour': 0.0435,
                        'price_month': 27.09,
                    },
                    {
                        'name': 'CCX33',
                        'VCPU': 8,
                        'RAM': 32,
                        'disk': 240,
                        'disk_type': 'NVME SSD',
                        'traffic': 30,
                        'price_hour': 0.0867,
                        'price_month': 54.09,
                    },
                    {
                        'name': 'CCX43',
                        'VCPU': 16,
                        'RAM': 64,
                        'disk': 360,
                        'disk_type': 'NVME SSD',
                        'traffic': 40,
                        'price_hour': 0.1725,
                        'price_month': 107.59,
                    },
                    {
                        'name': 'CCX53',
                        'VCPU': 32,
                        'RAM': 128,
                        'disk': 600,
                        'disk_type': 'NVME SSD',
                        'traffic': 50,
                        'price_hour': 0.3431,
                        'price_month': 214.09,
                    },
                    {
                        'name': 'CCX63',
                        'VCPU': 48,
                        'RAM': 192,
                        'disk': 960,
                        'disk_type': 'NVME SSD',
                        'traffic': 60,
                        'price_hour': 0.5138,
                        'price_month': 320.59,
                    }
                ]
            }
        ]
    })


with app.app_context():
    db_instance.create_db()

if __name__ == '__main__':
    app.run()
