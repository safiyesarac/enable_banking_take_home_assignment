#!/bin/bash


KEY_DIR="keys"
mkdir -p $KEY_DIR

openssl genpkey -algorithm RSA -out $KEY_DIR/private_key.pem -pkeyopt rsa_keygen_bits:2048

openssl rsa -pubout -in $KEY_DIR/private_key.pem -out $KEY_DIR/public_key.pem

echo "RSA key pair generated."
echo "Private key: $KEY_DIR/private_key.pem"
echo "Public key: $KEY_DIR/public_key.pem"
