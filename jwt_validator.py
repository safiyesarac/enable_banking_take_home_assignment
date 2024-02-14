from os import name
from flask import Flask, request, jsonify
import jwt
import requests

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

def validate_jwt(token):
    try:
        
        unverified_header = jwt.get_unverified_header(token)
        x5u_url = unverified_header.get("x5u")

     
        with open('keys/public_key.pem', 'r') as f:
            public_key = f.read()

        
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