<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">Enterprise-Grade Private AI Platform (v1.3.0)</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage). Approximately 90% of the release notes, README, and commit messages were generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) and [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service on an independent EC2 instance using Docker Compose, enabling easy deployment with Terraform.

## 🚀 Project Overview

AMATERASU is an enterprise-grade private AI platform. Built on AWS Bedrock, it allows you to develop and operate LLM-based applications in a secure and scalable environment. Integration with GitLab streamlines version control, CI/CD pipelines, and project management.


## ✨ Key Features

### Secure Foundation
- Secure LLM foundation based on AWS Bedrock
- Operation in a fully closed environment
- Enterprise-grade security

### Microservice Architecture
- Independent service components
- Container-based deployment
- Flexible scaling

### Infrastructure as Code
- Fully automated deployment using Terraform
- Environment-specific configuration management
- Version-controlled configuration

### GitLab Integration
- Enhanced version control, CI/CD pipelines, and project management capabilities
- Integration with self-hosted GitLab instances


## 🏗 System Architecture

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
- CI pipeline and GitLab Runner
- Backup and restore functionality
- LDAP/Active Directory integration
- Customizable authentication and access control

### 5. FG-prompt-pandora (Fargate Sample Application)
- Auto-scaling on AWS Fargate
- Prompt generation using Claude-3.5-Sonnet
- Intuitive UI based on Streamlit
- Easy deployment with a simple Docker image
- Integration sample for the AMATERASU environment

## 🔧 Deployment Guide

### Prerequisites
- AWS account
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

3. Deploy infrastructure
```bash
cd spellbook/base-infrastructure
terraform init && terraform apply

cd ../open-webui/terraform/main-infrastructure
terraform init && terraform apply

cd ../../litellm/terraform/main-infrastructure
terraform init && terraform apply

cd ../../langfuse/terraform/main-infrastructure
terraform init && terraform apply
```

4. Start services
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

2. Set environment variables: Edit the `.env` file and set the necessary environment variables such as `GITLAB_HOME`, `GITLAB_HOSTNAME`, `GITLAB_ROOT_PASSWORD`.

3. Start GitLab:
```bash
docker-compose up -d
```

4. Set up backups (optional): Create a backup directory and run the `docker-compose exec gitlab gitlab-backup create` command to perform a backup.


## 📈 Operational Management

### Monitoring
- Metrics collection with Prometheus
- Usage analysis with Langfuse
- Resource monitoring with CloudWatch

### Scheduling
- Automatic start/stop from 8:00 AM to 10:00 PM on weekdays
- Manual scaling according to demand
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
- Usage visualization and analysis
- Cost management and resource optimization
- Provision of a secure development environment


## 🆕 What's New

### AMATERASU v1.3.0 (Latest Release)

- 🎉 Added definition and status check of VPC, subnet, and Route53 zone data sources.
- 🎉 Added Elastic IP allocation and security group rules.
- 🎉 Added Route53 Private Hosted Zone domain name variable, added output value, and added variable definition.
- 🎉 Added Route53 Private Hosted Zone module.
- 🎉 Added private zone information to Route53 output.
- 🎉 Created records for private and public zones.
- 🎉 Improved Route53 output and simplified ALB output.
- 🎉 Integrated public and internal ALBs into a single ALB.
- 🎉 Added permission for access from within the VPC to the ALB security group.
- 🎉 Added method for obtaining the initial GitLab password.
- 🎉 Added Maki NOTE PC to the whitelist.
- 🚀 Resized the GitLab instance, corrected the path of the environment variable file, simplified the GitLab Docker Compose settings, and fixed the hostname.
- 🚀 Adjusted the EC2 instance startup schedule, changed the target ID of the ALB target group to the private IP.
- 🐛 Fixed attachment to the ALB target group.
- ⚠️ Updated the whitelist IP address.


## 📄 License

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

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

Build your enterprise-grade AI platform with AMATERASU. ✨