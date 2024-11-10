#!/bin/bash

# Update package index and install necessary packages
sudo apt-get update
sudo apt-get install -y ca-certificates curl git

# Create directory for APT keyrings
sudo install -m 0755 -d /etc/apt/keyrings

# Download and add Docker's official GPG key
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository to APT sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again after adding new repository
sudo apt-get update

# Install Docker and related packages
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make Docker Compose executable
sudo chmod +x /usr/local/bin/docker-compose

# Clone the MOA
git clone https://github.com/Sunwood-ai-labs/moa.git /home/ubuntu/moa

# Create .env file
# Note: The content of the .env file should be provided by Terraform
echo "${env_content}" > /home/ubuntu/moa/.env

# Set correct permissions for the .env file
chown ubuntu:ubuntu /home/ubuntu/moa/.env
chmod 600 /home/ubuntu/moa/.env

# Change to the MOA directory
cd /home/ubuntu/moa

# Run docker-compose with the specified file
sudo docker-compose -f docker-compose.ollama.yml up -d

echo "MOA setup completed and docker-compose started!"
