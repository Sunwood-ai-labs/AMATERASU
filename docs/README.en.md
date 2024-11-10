<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
<h1 align="center">🌄 AMATERASU v0.2.0 🌄</h1>
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU">
    <img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases">
    <img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/AMATERASU?style=social">
  </a>
</p>

<h2 align="center">
  ～ Automated Construction of an LLM Platform on AWS ～
</h2>

>[!IMPORTANT]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service on a separate EC2 instance using Docker Compose, enabling easier deployment with Terraform.

## 🚀 Project Overview

AMATERASU is an automation tool for building a Large Language Model (LLM) platform on AWS.  While inheriting functionality from MOA, it provides more flexible scaling and management by running each service on its own dedicated EC2 instance.

Key Features:
- Simple EC2 instance management using Terraform
- Independent EC2 instances and Docker Compose environments for each service
- Service-level scaling and operation
- Secure communication and access control

## ✨ Main Features

- None (at this time)


## 🔧 Usage

Follow the installation instructions and usage guidelines provided in this README to set up AMATERASU.


## 📦 Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit the .env file and configure the necessary credentials
```

3. Initialize and run Terraform:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## 🆕 Latest News

v0.2.0 features a revamped architecture, with each AI service now running in a separate EC2 instance using Docker Compose. This improves scalability and manageability of individual services.  The English README has also been updated, and images have been added to improve the appearance of the release notes.

With the architecture overhaul, the README now includes an architecture diagram (not included in this translation), system requirements, installation instructions, module structure, deployment methods, example operational commands, detailed directory structure for each module, examples of the Docker Compose configuration file (`docker-compose.yml`) and environment variable file (`.env`), scripts for SSH connection to each module, and Docker Compose service management (start, stop, log display). For enhanced security, each EC2 instance is protected by a dedicated security group, and inter-service communication is controlled within the internal VPC network.


## 🌐 Module Structure

Each module runs using Docker Compose on a separate EC2 instance:

### open-webui Module (EC2 Instance)
```
📁 open-webui/
├── 📄 docker-compose.yml  # open-webui and ollama configuration
├── 📄 .env               # Environment variable settings
└── 📁 config/            # Configuration files
```

Example configuration (docker-compose.yml):
```yaml
version: '3'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ./data:/root/.ollama

  open-webui:
    image: open-webui/open-webui
    ports:
      - "3000:3000"
    environment:
      - OLLAMA_URL=http://ollama:11434
```

### litellm Module (EC2 Instance)
```
📁 litellm/
├── 📄 docker-compose.yml  # litellm service configuration
├── 📄 .env               # API key and other environment variables
└── 📁 config/            # LLM configuration files
```

### langfuse Module (EC2 Instance)
```
📁 langfuse/
├── 📄 docker-compose.yml  # langfuse and DB configuration
├── 📄 .env               # Environment variable settings
└── 📁 data/              # PostgreSQL data
```

## 🔨 Deployment Command Examples

Deploying only specific modules:
```bash
# Deploy only the open-webui module
terraform apply -target=module.ec2_open_webui

# Deploy only the litellm module
terraform apply -target=module.ec2_litellm

# Deploy only the langfuse module
terraform apply -target=module.ec2_langfuse
```

## 💻 Module Management Commands

Connecting to each EC2 instance:
```bash
# SSH connection script
./scripts/connect.sh open-webui
./scripts/connect.sh litellm
./scripts/connect.sh langfuse
```

Docker Compose operations:
```bash
# Run within each instance
cd /opt/amaterasu/[module-name]
docker-compose up -d      # Start service
docker-compose down      # Stop service
docker-compose logs -f   # Display logs
```

## 🔒 Security Configuration

- Each EC2 instance is protected by a dedicated security group.
- Inter-service communication is controlled within the internal VPC network.
- Only the minimum necessary ports are exposed.
- Permission management using IAM roles.

## 📚 Directory Structure

```plaintext
amaterasu/
├── terraform/          # Terraform code
│   ├── modules/        # Modules for each EC2 instance
│   ├── main.tf        # Main configuration
│   └── variables.tf   # Variable definitions
├── modules/           # Docker Compose configuration for each service
│   ├── open-webui/    # open-webui related files
│   ├── litellm/      # litellm related files
│   └── langfuse/     # langfuse related files
├── scripts/          # Operational scripts
└── docs/            # Documentation
```

## ⚠️ Important Changes

- Due to the revamped architecture, upgrading from previous versions requires manual migration following the provided steps.  Refer to the upgrade instructions for details.


## 📦 Upgrade Instructions

1. Stop the existing environment.
2. Build the environment with the new architecture following the instructions in this README.
3. If data migration is necessary, perform the appropriate steps. (Specific steps are not provided.)


## 📄 License

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgements

Thanks to iris-s-coon and Maki.

## 🤝 Contributions

Contributions are welcome!  Here's how to get involved:

1. Fork this repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Create a pull request

## 📧 Support

For questions or feedback, please feel free to contact us:
- Create an issue: [GitHub Issues](https://github.com/Sunwood-ai-labs/AMATERASU/issues)
- Email: support@sunwoodai.com

Build a more flexible and powerful AI infrastructure with AMATERASU! ✨