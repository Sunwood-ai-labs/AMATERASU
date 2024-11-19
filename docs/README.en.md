<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
<h1 align="center">🌄 AMATERASU v0.4.0 🌄</h1>
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
  ～ Automates the Construction of an LLM Platform on AWS ～
</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage).  Approximately 90% of the release notes, README, and commit messages are generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) and [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service on an independent EC2 instance using Docker Compose, allowing for easier deployment with Terraform.

## 🚀 Project Overview

AMATERASU is an automation tool for building an LLM (Large Language Model) platform on AWS.  Building upon the functionality of MOA, it achieves more flexible scaling and management by operating each service on an independent EC2 instance.

Key Features:
- Simple EC2 instance management using Terraform
- Independent EC2 instance and Docker Compose environment for each service
- Service-level scaling and operation
- Secure communication and access control

## ✨ Main Features

- Automated AWS infrastructure construction using Terraform
- Containerization and management of each service using Docker Compose
- Integration with multiple LLM models (OpenAI, Anthropic, Gemini, etc.)
- Model management and billing features using Langfuse


## 🔧 Usage

Follow the installation instructions and usage guide provided in this README to set up AMATERASU.


## 📦 Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit the .env file and configure the necessary credentials (LITELLM_MASTER_KEY, LITELLM_SALT_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GEMINI_API_KEY_IRIS, etc.)
```

3. Initialize and run Terraform:
```bash
cd spellbook/open-webui/terraform
terraform init
terraform plan
terraform apply
```


## SSH

Refer to the `instance_public_ip` output value in `spellbook/open-webui/terraform/main-infra/outputs.tf` for the SSH connection IP address.


## 🆕 What's New

### v0.4.0 Update Notes

- Added infrastructure construction functionality using existing VPCs and security groups. This simplifies integration with existing environments, reducing infrastructure costs and time.
- Updated the English README and fixed several bugs.
- Added variables for existing VPC and subnet IDs for flexible adaptation to existing environments.
- Modified the settings to use existing security groups.
- Added a whitelist function to the security group (using the `whitelist.csv` file).
- Added configuration for ALB, target groups, listeners, and CloudFront Distribution.
- Configured the Terraform variable file (AWS region, project name, environment name, etc.).
- Added configuration for key output values (VPC ID, subnet ID, etc.).
- Added functionality to build VPCs, subnets, internet gateways, and NAT gateways.
- Simplified the security group description.


## ⚠️ Important Changes

- Because the system has been changed to use existing VPCs and subnets, upgrading from previous versions requires manual migration.  Specific instructions are not provided.


## 📦 Upgrade Instructions

Specific upgrade instructions are not provided. Refer to the Important Changes section.


## 👏 Acknowledgements

Thanks to iris-s-coon and Maki for their contributions.


## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributions

Contributions are welcome!  You can participate by following these steps:

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