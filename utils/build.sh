#!/bin/bash
set -e

# Přejdeme do složky utils, kde tento skript reálně leží
cd "$(dirname "$0")"

# 1. Sestavení Docker obrazu (kontext je aktuální složka utils)
docker build -t openssl-generator .

# 2. Spuštění kontejneru, namountování kořene projektu (..) do /work a okamžitý úklid
docker run --rm -v "$(pwd)/..:/work" openssl-generator sh -c 
