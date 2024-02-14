from os import name
from flask import Flask, request, jsonify
import jwt
import requests
from flask import send_from_directory

jwt_validator = Flask(__name__)

from flask_swagger_ui import get_swaggerui_blueprint

# Swagger UI configuration
SWAGGER_URL = '/swagger-ui' 
API_URL = '/static/swagger.json' 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "JWT Validator API"
    }
)

jwt_validator.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@jwt_validator.route('/keys/public_key.pem')
def serve_public_key():
    return send_from_directory('keys', 'public_key.pem')

def validate_jwt(token):
    try:
        
        unverified_header = jwt.get_unverified_header(token)
        x5u_url = unverified_header.get("x5u")
        if not x5u_url:
            return False, "Missing x5u parameter in JWT header."

        # Fetch the PEM-encoded X.509 certificate from the x5u URL
        response = requests.get(x5u_url)
        if response.status_code != 200:
            return False, f"Failed to fetch certificate from x5u URL. Status code: {response.status_code}"
        public_key = response.text

        decoded = jwt.decode(token, public_key, algorithms=["RS256"], options={"verify_exp": True})
        return True, None  # JWT is valid
    except jwt.ExpiredSignatureError:
        return False, "JWT has expired."
    except jwt.InvalidTokenError as e:
        return False, str(e)
    except Exception as e:
        return False, f"An error occurred during JWT validation: {str(e)}"

@jwt_validator.route('/auth', methods=['GET'])
def auth():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"valid": False, "error": "Authorization header is missing."}), 400
    token = auth_header.split(" ")[1]
    is_valid, error = validate_jwt(token)
    if is_valid:
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False, "error": error}), 400
if name == "main":
    jwt_validator.run(debug=True)