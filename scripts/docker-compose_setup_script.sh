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

# Create the docker group if it doesn't exist
sudo groupadd -f docker

# Add current user to the docker group
sudo usermod -aG docker $USER

# Apply the new group membership
echo "Docker group membership has been added."
echo "You need to log out and log back in (or restart the system) for the group membership to take effect."

# Optionally, start and enable the Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Install uv - the Python package installer from astral.sh
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Docker, docker-compose, and uv setup completed!"
echo "After logging out and back in, you'll be able to run Docker commands without sudo."
echo "uv should be available immediately. If not, you may need to source your profile or restart your terminal."
