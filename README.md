## Generating RSA Keys for JWT Signing and Verification

For testing and development purposes, you can generate your RSA key pair (private and public keys) using the provided script `generate_keys.sh`. This is necessary for signing JWTs and verifying their signatures.

### How to Generate Keys

1. Ensure you have OpenSSL installed on your machine. It's required by the script to generate the RSA keys.

2. Run the script from the project's root directory:

```bash
./generate_keys.sh
```

# JWT Validator API

This API provides a service for validating JSON Web Tokens (JWT) using the RS256 algorithm. It includes a Swagger UI for easy interaction and testing.

## Prerequisites

- Python 3.8 or higher
- OpenSSL (for generating RSA keys)
- Pip for installing Python packages

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/safiyesarac/jwt-validator-api.git
cd jwt-validator-api```


### Create and Activate a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate```