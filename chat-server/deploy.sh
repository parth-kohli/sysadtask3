#!/bin/bash
set -e
IMAGE_NAME="pkohli33/chat-server"
VERSION_TAG="latest"
echo "[*] Pulling latest image..."
docker pull $IMAGE_NAME:$VERSION_TAG
echo "[*] Restarting services..."
docker-compose down
docker-compose up -d
echo "[+] Deployment complete."
