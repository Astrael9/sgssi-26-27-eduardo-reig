#!/bin/bash
# Uso: ./cifrar.sh <archivo> <clave_publica.pem>

FICHERO="$1"
CLAVE_PUB="$2"

if [ "$#" -ne 2 ] || [ ! -f "$FICHERO" ] || [ ! -f "$CLAVE_PUB" ]; then
    echo "Error: Parametros o archivos no validos." >&2
    echo "Uso: $0 <archivo> <clave_publica.pem>" >&2
    exit 1
fi

# 1. Generar una clave simétrica aleatoria de 32 bytes (256 bits) para AES
openssl rand 32 > clave_aes.key

# 2. Cifrar el archivo con AES-256-ECB usando la clave simétrica
openssl enc -aes-256-ecb -in "$FICHERO" -out "${FICHERO}.enc" \
    -K $(xxd -p -c 64 clave_aes.key)

# 3. Cifrar únicamente la clave AES con la clave pública RSA (OAEP)
openssl pkeyutl -encrypt -pubin -inkey "$CLAVE_PUB" \
    -pkeyopt rsa_padding_mode:oaep \
    -in clave_aes.key -out clave_aes.key.enc

# 4. Eliminar la clave AES en texto plano por seguridad
rm -f clave_aes.key

echo "Cifrado completado."
echo "Archivos a enviar: ${FICHERO}.enc y clave_aes.key.enc"