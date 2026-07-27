#!/bin/bash
set -e

rm -rf tmp_gen

export GIT_TERMINAL_PROMPT=0

if [ ! -f "skip-server/scripts/create_ca.sh" ]; then
  echo "Skip folder is empty, trying to load submodule..."
  
  git submodule update --init --recursive 2>/dev/null || true
  
  if [ ! -f "skip-server/scripts/create_ca.sh" ]; then
    echo "🔄 Cloning from github..."
    rm -rf skip-server
    git clone https://github.com/waustin14/SKIP-Server.git skip-server
  fi
fi

chmod +x skip-server/scripts/*.sh
sed -i 's/\r$//' skip-server/scripts/*.sh 2>/dev/null || true

echo "Generating keys and certs using custom OpenSSL (neliba/openssl:3.6.3)..."
mkdir -p src/config/skip1/config src/config/skip1/certs/ca src/config/skip1/secrets
mkdir -p src/config/skip2/config src/config/skip2/certs/ca src/config/skip2/secrets
mkdir -p src/config/client1
mkdir -p src/config/client2
mkdir -p tmp_gen/ca

docker run --rm -v "$(pwd):/work" -w /work neliba/openssl:3.6.3 bash -c "
  cd skip-server
  
  echo 'Creating CA...'
  ./scripts/create_ca.sh ../tmp_gen/ca

  echo '📜 Generating server certs...'
  ./scripts/sign_server_cert.sh -c ../tmp_gen/ca/ca.pem -k ../tmp_gen/ca/ca.key -o ../tmp_gen skip1.cml.lab 'skip1.cml.lab,skip1,localhost' '10.0.0.10,192.168.1.254,127.0.0.1'
  ./scripts/sign_server_cert.sh -c ../tmp_gen/ca/ca.pem -k ../tmp_gen/ca/ca.key -o ../tmp_gen skip2.cml.lab 'skip2.cml.lab,skip2,localhost' '10.0.0.20,192.168.2.254,127.0.0.1'

  echo 'Generating ML-KEM...'
  ./scripts/generate_mlkem_kp.sh -p ../tmp_gen/skip1_kem_pub.pem -s ../tmp_gen/skip1_kem_priv.pem
  ./scripts/generate_mlkem_kp.sh -p ../tmp_gen/skip2_kem_pub.pem -s ../tmp_gen/skip2_kem_priv.pem

  echo 'Generating PSK...'
  ./scripts/create_psk.sh -i client1 -f ../tmp_gen/psk_skip1.txt
  ./scripts/create_psk.sh -i client2 -f ../tmp_gen/psk_skip2.txt
"

echo "Certificate and keys distribution..."

cp tmp_gen/ca/ca.pem src/config/skip1/certs/ca/ca.pem
cp tmp_gen/skip1.cml.lab.pem.crt src/config/skip1/certs/skip1.pem.crt
cp tmp_gen/skip1.cml.lab_key.pem src/config/skip1/certs/skip1_key.pem
cp tmp_gen/skip1_kem_pub.pem src/config/skip1/secrets/kem_pub.pem
cp tmp_gen/skip1_kem_priv.pem src/config/skip1/secrets/kem_priv.pem
cp tmp_gen/skip2_kem_pub.pem src/config/skip1/secrets/skip2_kem_pub.pem
cp tmp_gen/psk_skip1.txt src/config/skip1/secrets/psk.txt
cp tmp_gen/psk_skip1.txt src/config/client1/psk.txt

cp tmp_gen/ca/ca.pem src/config/skip2/certs/ca/ca.pem
cp tmp_gen/skip2.cml.lab.pem.crt src/config/skip2/certs/skip2.pem.crt
cp tmp_gen/skip2.cml.lab_key.pem src/config/skip2/certs/skip2_key.pem
cp tmp_gen/skip2_kem_pub.pem src/config/skip2/secrets/kem_pub.pem
cp tmp_gen/skip2_kem_priv.pem src/config/skip2/secrets/kem_priv.pem
cp tmp_gen/skip1_kem_pub.pem src/config/skip2/secrets/skip1_kem_pub.pem
cp tmp_gen/psk_skip2.txt src/config/skip2/secrets/psk.txt
cp tmp_gen/psk_skip2.txt src/config/client2/psk.txt

rm -rf tmp_gen

echo "Building & Running Docker..."
docker compose up --build
