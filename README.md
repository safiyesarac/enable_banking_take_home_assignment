# JWT Validator API

## Description

This JWT Validator API is designed to validate JSON Web Tokens (JWT) using the RS256 algorithm. The API expects JWTs to have an `x5u` header pointing to a URL where a PEM-encoded public key can be retrieved for signature verification.

## Getting Started

### Prerequisites

- Python 3.8+
- OpenSSL for generating RSA key pairs
- A server to host your public key

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/<your-github-username>/jwt-validator-api.git
    cd jwt-validator-api
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Generate RSA key pair:
    ```sh
    ./generate_keys.sh
    ```

### Hosting the Public Key

1. Host your `public_key.pem` file on a server or a service that allows you to serve static files (e.g., GitHub, Amazon S3).
2. Take note of the URL that points directly to your `public_key.pem` file.

### Configuration

1. Update the JWT generation script to include the `x5u` header with the URL of your hosted public key.
2. Ensure the Flask application's `validate_jwt` function is correctly set up to fetch the public key from the provided URL.

### Running the Application

1. Start the Flask app:
    ```sh
    flask run
    ```
    or directly with Python:
    ```sh
    python app.py
    ```

2. Access the Swagger UI by navigating to:
    ```
    http://localhost:5000/swagger-ui
    ```

### Using the API

1. To validate a JWT, make a GET request to the `/auth` endpoint with the `Authorization` header set to `Bearer <jwt>`.
2. The response will indicate whether the JWT is valid or not.

### Testing

Run the automated test suite with:
```sh
python -m unittest
```