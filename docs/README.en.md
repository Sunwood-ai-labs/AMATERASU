<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
<h1 align="center">🌄 AMATERASU v0.3.0 🌄</h1>
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
  ～ Automating the Construction of an LLM Platform on AWS ～
</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), and approximately 90% of the release notes, README, and commit messages were generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) + [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service on a separate EC2 instance using Docker Compose, enabling easier deployment with Terraform.

## 🚀 Project Overview

AMATERASU is an automation tool for building an LLM (Large Language Model) platform on AWS.  While inheriting functionality from MOA, it offers more flexible scaling and management by running each service on its own independent EC2 instance.

Key Features:
- Simple EC2 instance management using Terraform
- Independent EC2 instances and Docker Compose environments for each service
- Service-level scaling and operation
- Secure communication and access control

## ✨ Main Features

- Automated AWS infrastructure build with Terraform
- Containerization and management of each service using Docker Compose
- Integration with multiple LLM models (OpenAI, Anthropic, Gemini, etc.)
- Model management and billing functionality using Langfuse


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
# Edit the .env file and set the necessary credentials (LITELLM_MASTER_KEY, LITELLM_SALT_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, GEMINI_API_KEY_IRIS, etc.)
```

3. Initialize and run Terraform:
```bash
cd spellbook/open-webui/terraform
terraform init
terraform plan
terraform apply
```


## SSH

```bash
ssh -i "C:\Users\makim\.ssh\AMATERASU-terraform-keypair-tokyo-PEM.pem" ubuntu@i-0f2dd4596a0e1f3c0
```

## 🆕 Latest Updates

### v0.3.0 Changes

- README.md update: Clarified the use of SourceSage and Claude.ai, emphasizing important information.
- Added multiple Claude model definitions: Expanded the Claude models available through Langfuse. (`claude-3.5-haiku-20241022`, `claude-3.5-haiku-latest`, `claude-3.5-sonnet-20240620`, `claude-3.5-sonnet-20241022`, `claude-3.5-sonnet-latest`, `claude-3-haiku-20240307`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`)
- Added environment variable settings for LLaMA model integration: Facilitated integration with various LLaMA model providers. (`LITELLM_MASTER_KEY`, `LITELLM_SALT_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GEMINI_API_KEY_IRIS`)
- Added SSH connection information and infrastructure description updates to README.md: Added instructions for SSH connection to the EC2 instance and information about the architecture refresh in v0.2.0.
- Updated English README
- Corrected volume mounts in docker-compose.yml
- Changed logging library: Switched from the `logging` module to the `loguru` module.


## 📄 License

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgements

Thanks to iris-s-coon and Maki for their contributions.

## 🤝 Contributions

Contributions are welcome!  To contribute:

1. Fork this repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Create a pull request

## 📧 Support

For questions or feedback, please feel free to contact us:
- Create an Issue: [GitHub Issues](https://github.com/Sunwood-ai-labs/AMATERASU/issues)
- Email: support@sunwoodai.com

Build a more flexible and powerful AI infrastructure with AMATERASU! ✨