<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">Enterprise-Grade Private AI Platform (v1.14.0)</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), and approximately 90% of the release notes, README, and commit messages were generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) + [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service in an independent EC2 instance using Docker Compose, enabling easy deployment with Terraform.

## 🚀 Project Overview

AMATERASU is an enterprise-grade private AI platform. Built on AWS Bedrock and Google Vertex AI, it allows you to develop and operate LLM-based applications in a secure and scalable environment.  Integration with GitLab streamlines version control, CI/CD pipelines, and project management.  v1.14.0 includes Terraform code to simplify the construction and management of AWS infrastructure, and a module for easier CloudFront infrastructure setup.  Setup scripts and output value definitions have been added to improve Dify setup and operation.

This repository is structured as a "spellbook" for managing multiple AI-related projects. Each project is organized as a separate folder for deploying and managing specific AI services or functionalities.

## ✨ Key Features

### Secure Foundation
- Secure LLM foundation based on AWS Bedrock and Google Vertex AI
- Operation in a completely closed environment
- Enterprise-grade security

### Microservice Architecture
- Independent service components
- Container-based deployment
- Flexible scaling

### Infrastructure as Code
- Fully automated deployment with Terraform
- Environment-specific configuration management
- Version-controlled infrastructure

### GitLab Integration
- Enhanced version control, CI/CD pipelines, and project management capabilities
- Integration with a self-hosted GitLab instance
- LLM-powered merge request analysis
- Automated labeling using GitLab Webhooks

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
                CD["Coder<br/>Cloud Development Environment"]
            end
            
            subgraph "Fargate-based Service"
                PP["Prompt Pandora<br/>Prompt Generation Support"]
                ECS["ECS Fargate Cluster"]
            end
        end
        
        subgraph "Infrastructure Layer"
            CF["CloudFront"]
            WAF["WAF"]
            R53["Route 53"]
        end
        
        subgraph "AWS Services"
            Bedrock["AWS Bedrock<br/>LLM Service"]
            IAM["IAM<br/>Authentication & Authorization"]
        end
        
        OW --> CF
        LL --> CF
        LF --> CF
        GL --> CF
        CD --> CF
        PP --> ECS
        
        CF --> WAF
        WAF --> R53
        
        EC2 --> Bedrock
        ECS --> Bedrock
        EC2 --> IAM
        ECS --> IAM
    end
```

## 📦 Component Composition

### 1. Open WebUI (Frontend)
- Chat-based user interface
- Responsive design
- Prompt template management
    - [Details here](./spellbook/open-webui/README.md)

### 2. LiteLLM (API Proxy)
- Unified access to Claude-3 series models
- Access to Google Vertex AI models
- API key management and rate limiting
    - [Details here](./spellbook/litellm/README.md)

### 3. Langfuse (Monitoring)
- Usage tracking
- Cost analysis
- Performance monitoring
    - [Details here](./spellbook/langfuse3/README.md)

### 4. GitLab (Version Control)
- Self-hosted GitLab instance
- Project and code management
- CI pipeline and Runner configuration
- Backup and restore functionality

### 5. FG-prompt-pandora (Fargate Sample Application)
- Auto-scaling on AWS Fargate
- Prompt generation using Claude-3.5-Sonnet
- Intuitive UI based on Streamlit
    - [Details here](./spellbook/fg-prompt-pandora/README.md)

### 6. Coder (Cloud Development Environment)
- Web-based IDE environment
- Support for VS Code extensions
- Secure development on AWS infrastructure
    - [Details here](./spellbook/Coder/README.md)

### 7. Dify (AI Application Development Platform)
- AI application development platform integrating various AI models
- UI/API-based development
    - [Details here](./spellbook/dify/README.md)

### 8. Dify Beta (AI Application Development Platform)
- Beta version of Dify including new and experimental features
- Advanced configuration of vector databases and sandbox environments
    - [Details here](./spellbook/dify-beta1/README.md)

### 9. Open WebUI Pipeline
- Pipeline features enhancing integration with Open WebUI
- Allows filter processing such as conversation turn limits and Langfuse integration
    - [Details here](./spellbook/open-webui-pipeline/README.md)

### 10. tfvars_generator (Terraform Variable Generator)
- Web application that automatically generates Terraform variable files (`terraform.tfvars`)
- Supports project detection, common settings, and individual settings
    - [Details here](./spellbook/tfvars_generator/README.md)

## 🆕 What's New

### AMATERASU v1.14.0 (Latest Release)

- 🎉 **Setup script implementation:** Automates cloning the AMATERASU repository, setting environment variables, and starting applications using Docker Compose after launching EC2 instances.
- 🎉 **Terraform configuration for CloudFront infrastructure module:** Implemented a Terraform module to manage CloudFront distributions, WAFv2, Route53 records, and ACM certificates.
- 🎉 **Added Terraform code for main infrastructure construction:** Integrated IAM, Compute, and Networking modules into the main Terraform file.
- 🎉 **Defined output values for built infrastructure:** Defined output values for the built infrastructure resources.
- 🎉 **Added variables for CloudFront infrastructure:** Added variables required for configuring the CloudFront infrastructure.
- 🎉 **Created and configured a common variable file:** Defined variables used commonly across all infrastructure resources in `common_variables.tf`, improving modularity and reusability of resource definitions.


## 🛠️ Usage

Refer to the individual README files for instructions on using each component.  Specifically, see `spellbook/tfvars_generator/README.md` for instructions on using the Terraform variable generator web app.


## 📦 Installation Instructions

1. Clone the repository:
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```
2. Follow the instructions in each project's README to install dependencies and deploy the application.
3. Enter the necessary settings in the `terraform.tfvars` file.

## 📦 Dependencies

The root directory of this repository contains a `requirements.txt` file defining common dependencies.
```bash
pip install -r requirements.txt
```

```plaintext
aira
sourcesage
```

## 📄 License

This project is licensed under the MIT License.

## 👏 Acknowledgements

Thanks to Maki and iris-s-coon for their contributions.