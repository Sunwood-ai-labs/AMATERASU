<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">Enterprise-Grade Private AI Platform (v1.6.1)</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage).  Approximately 90% of the release notes, README, and commit messages were generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) and [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has been enhanced to run each AI service as an independent EC2 instance using Docker Compose, enabling easier deployment with Terraform.


## 🚀 Project Overview

AMATERASU is an enterprise-grade private AI platform.  Built on AWS Bedrock, it allows you to develop and operate LLM-powered applications in a secure and scalable environment.  Integration with GitLab streamlines version control, CI/CD pipelines, and project management.  AMATERASU v1.6.1 adds test scripts for Bedrock Nova models, along with several other enhancements and bug fixes.


## ✨ Key Features

### Secure Foundation
- Secure LLM foundation based on AWS Bedrock
- Operation in a fully closed environment
- Enterprise-grade security

### Microservices Architecture
- Independent service components
- Container-based deployment
- Flexible scaling

### Infrastructure as Code
- Fully automated deployment using Terraform
- Environment-specific configuration management
- Version-controlled infrastructure

### GitLab Integration
- Enhanced version control, CI/CD pipelines, and project management features
- Integration with self-hosted GitLab instances
- LLM-powered merge request analysis
- Automated labeling service using GitLab Webhooks


## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "Application Layer"
            subgraph "EC2-based Services"
                OW["Open WebUI<br/>Chat Interface"]
                LL["LiteLLM Proxy<br/>API Proxy"]
                LF["Langfuse<br/>Monitoring"]
                GL["GitLab<br/>Version Control"]
            end
            
            subgraph "Fargate-based Service"
                PP["Prompt Pandora<br/>Prompt Generation Support"]
                ECS["ECS Fargate Cluster"]
            end
        end
        
        subgraph "Infrastructure Layer<br>(AMATERASU Architecture)"
            ALB["Application Load Balancer"]
            EC2["EC2 Instances"]
            SG["Security Groups"]
            R53["Route 53"]
            ACM["ACM Certificates"]
            ECR["Elastic Container Registry"]
        end
        
        subgraph "AWS Services"
            Bedrock["AWS Bedrock<br/>LLM Service"]
            IAM["IAM<br/>Authentication & Authorization"]
        end
        
        OW --> ALB
        LL --> ALB
        LF --> ALB
        GL --> ALB
        PP --> ECS
        ECS --> ALB
        ALB --> EC2
        ALB --> ECS
        EC2 --> SG
        ECS --> SG
        R53 --> ALB
        ACM --> ALB
        ECR --> ECS
        EC2 --> Bedrock
        ECS --> Bedrock
        EC2 --> IAM
        ECS --> IAM
    end

    Users["Enterprise Users"] --> R53
```

## 📦 Component Composition

### 1. Open WebUI (Frontend)
- Chat-based user interface
- Responsive design
- Prompt template management

### 2. LiteLLM (API Proxy)
- Unified access to Claude-3 series models
- API key management
- Rate limiting and load balancing

### 3. Langfuse (Monitoring)
- Usage tracking
- Cost analysis
- Performance monitoring

### 4. GitLab (Version Control)
- Self-hosted GitLab instance
- Project and code management
- CI pipelines and GitLab Runner
- Backup and restore functionality
- LDAP/Active Directory integration
- Customizable authentication and access control

### 5. FG-prompt-pandora (Fargate Sample Application)
- Autoscaling on AWS Fargate
- Prompt generation using Claude-3.5-Sonnet
- Intuitive UI based on Streamlit
- Easy deployment with a simple Docker image
- Sample integration with the AMATERASU environment


## 🔧 Deployment Guide

### Prerequisites
- AWS Account
- Terraform >= 0.12
- Docker & Docker Compose
- AWS CLI configured

### Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```

2. Set environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Deploy infrastructure (You need to deploy the infrastructure for each service in the `spellbook` directory individually.)
```bash
cd spellbook/base-infrastructure
terraform init && terraform apply

cd ../open-webui/terraform/main-infrastructure
terraform init && terraform apply

cd ../../litellm/terraform/main-infrastructure
terraform init && terraform apply

cd ../../langfuse/terraform/main-infrastructure
terraform init && terraform apply

cd ../../gitlab/terraform/main-infrastructure
terraform init && terraform apply

cd ../../FG-prompt-pandora/terraform
terraform init && terraform apply
```

4. Start services (You need to start each service in the `spellbook` directory individually.)

```bash
# Langfuse
cd ../../../langfuse
docker-compose up -d

# LiteLLM
cd ../litellm
docker-compose up -d

# Open WebUI
cd ../open-webui
docker-compose up -d

# GitLab
cd ../gitlab
docker-compose up -d

# FG-prompt-pandora
cd ../FG-prompt-pandora
docker-compose up -d
```

### GitLab Setup

1. Create the environment configuration file:
```bash
cd spellbook/gitlab
cp .env.example .env
```

2. Set environment variables: Edit the `.env` file and set the necessary environment variables, such as `GITLAB_HOME`, `GITLAB_HOSTNAME`, `GITLAB_ROOT_PASSWORD`.

3. Start GitLab:
```bash
docker-compose up -d
```

4. Configure backups (optional): Create a backup directory and run the `docker-compose exec gitlab gitlab-backup create` command to perform a backup.


## 📈 Operations Management

### Monitoring
- Metrics collection with Prometheus
- Usage analysis with Langfuse
- Resource monitoring with CloudWatch

### Scheduling
- Automatic start/stop from 8:00 to 22:00 on weekdays
- Manual scaling based on demand
- Batch job scheduling

### Security
- IP whitelist control
- TLS/SSL encryption
- IAM role-based access control

## 💡 Use Cases

### Prompt Engineering Support
- Optimal prompt generation from task descriptions
- Suggestions for improving existing prompts
- Prompt template management and sharing
- Standardization of prompt quality across the team

### LLM Application Development
- Secure model access via API proxy
- Visualization and analysis of usage
- Cost management and resource optimization
- Provision of a secure development environment


## 🆕 What's New

### AMATERASU v1.6.1 (Latest Release)

- 🎉 **Added Bedrock Nova Model Test Scripts**: Added scripts to automate testing of Bedrock Nova models (`bedrock/nova-micro`, `bedrock/nova-lite`, `bedrock/nova-pro`).  Logs response time, content, and token usage. Uses `text2art` and `loguru` libraries.
- 🎉 **Expanded LiteLLM Configuration File and Added AWS Configuration**: Added OpenAI, Anthropic, Google Gemini, and AWS API key and credential fields to the `.env.example` file. AWS configuration includes access key ID, secret access key, and default region (Tokyo) settings.
- 🚀 **Removed Unnecessary Log Settings**: Removed unnecessary log settings from the `loguru` library for simplification.
- ⚠️  **Changed Bedrock Model Specification in `config.yaml` and Corrected Region Specification**: Changed notation like `bedrock/us.amazon.nova-micro-v1:0` to `bedrock/amazon.nova-micro-v1:0` and corrected the region specification for Bedrock models.


### AMATERASU v1.6.0 (Previous Release)

- 🎉 **Implemented LLM-powered Merge Request Analysis Feature**: Includes OpenAI API integration, prompt engineering for generating review results, saving analysis results to JSON files, defining data structures using data classes, error handling and logging, and configuration via environment variables.
    - Outputs reviews and improvement suggestions from the perspectives of code quality, security, testing, and architecture.
- 🎉 **Implemented Automated Labeling Service using GitLab Webhooks**: Includes a FastAPI-based webhook server, integration with the GitLab API and OpenAI API (via LiteLLM Proxy), automatic labeling of issues based on title and description using LLMs, ngrok setup for public URLs in development environments (development environment only), health check endpoints and logging, webhook token authentication, error handling and exception handling, preserving existing labels and adding new labels, enhanced logging, environment variable configuration management, type hints, and docstrings for improved code quality.
    - Automatically assigns appropriate labels using LLMs, triggered by issue events.
- 🚀 **Created README.md for GitLab service**: Describes directory structure and webhook settings.
- 🚀 **Created README.md for GitLab Runner**: Describes configuration, Runner registration, and precautions.
- 🚀 **Created README.md for the `services` directory**: Describes service composition and configuration management.
- 🚀 **Redesigned `services_header.svg`**: Added animation, changed gradient colors, and added shadows.
- 🚀 **Redesigned `agents_header.svg`**: Added animation, changed gradient colors, and added shadows.
- 🚀 **Created GitLab configuration directory**: Created a configuration directory.
- 🚀 **Created GitLab data directory**: Created a data directory.
- 🚀 **Created GitLab log directory**: Created a log directory.
- 🚀 **Created GitLab backup directory**: Created a backup directory.
- 🚀 **Created GitLab Runner configuration directory**: Created a configuration directory.
- 🚀 **Updated dependency libraries**: Updated versions of FastAPI, uvicorn, python-gitlab, openai, python-dotenv, pydantic, pyngrok, loguru, rich, and argparse.


## 📄 License

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for details.

## 🤝 Contributions

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Create a pull request

## 📞 Support

For questions or feedback, please contact us:
- GitHub Issues: [Issues](https://github.com/Sunwood-ai-labs/AMATERASU/issues)
- Email: support@sunwoodai.com

## 👏 Acknowledgements

Thanks to Maki and iris-s-coon for their contributions.

---

Build your enterprise-grade AI platform with AMATERASU! ✨