<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">Enterprise-Grade Private AI Platform (🚀 AMATERASU v1.23.0)</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), and approximately 90% of the release notes, README, and commit messages are generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) + [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service as an independent EC2 instance using Docker Compose, enabling easy deployment with Terraform.


## 🚀 Project Overview

AMATERASU is an enterprise-grade private AI platform. Built on AWS Bedrock and Google Vertex AI, it allows for the development and operation of LLM-based applications in a secure and scalable environment. Integration with GitLab streamlines version control, CI/CD pipelines, and project management. This repository serves as a "Spellbook" for managing multiple AI-related projects. Each project is structured as an independent folder for deploying and managing specific AI services or functionalities.


## ✨ Key Features

### Secure Foundation
- Secure LLM foundation based on AWS Bedrock and Google Vertex AI
- Operation in a completely closed environment
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
- Enhanced version control, CI/CD pipelines, and project management
- Integration with self-hosted GitLab instances
- LLM-powered merge request analysis
- Automated labeling using GitLab Webhooks

### Project Exploration Feature
- Automatic detection of Terraform projects and generation of `terraform.tfvars` files
- Simplified configuration using the `amaterasu` command-line tool


## 🏗️ System Architecture

![](docs/flow.svg)

- AMATERASU Base Infrastructure provides reusable base components, reducing costs and management overhead.
- Multi-layered security is achieved through different security groups (Default, CloudFront, VPC Internal, Whitelist) for various purposes.
- AMATERASU EC2 Module runs Docker containers on EC2 instances.
- AMATERASU EE Module uses an ECS cluster, deploying from the development environment to ECR for operation.
- Both modules are protected by CloudFront and WAF with IP whitelisting and share the same base infrastructure.
- The entire infrastructure is managed by a modularized design using Terraform, leveraging the same security groups and network settings.


## 📦 Component Composition

### 1. Open WebUI (Frontend)
- Chat-based user interface
- Responsive design
- Prompt template management
    - [Details here](./spellbook/open-webui/README.md)

### 2. LiteLLM (API Proxy)
- Unified access to Claude-3 series models
- Access to Google Vertex AI models
- OpenRouter API integration
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
- CI pipelines and Runner configuration
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
- Advanced settings for vector databases and sandbox environments
    - [Details here](./spellbook/dify-beta1/README.md)

### 9. Open WebUI Pipeline
- Pipeline functionality enhancing integration with Open WebUI
- Filter processing such as conversation turn limits and Langfuse integration
    - [Details here](./spellbook/open-webui-pipeline/README.md)

### 10. Amaterasu Tool (Terraform Variable Generator)
- Automates the generation of `terraform.tfvars` files using a command-line tool
- Generates configuration values for each project in the spellbook
    - [Details here](./spellbook/amaterasu-tool-ui/README.md)

### 11. Kotaemon (Document and Chat RAG UI Tool)
- RAG UI tool for interacting with documents and chat
- Provides Docker environment and Terraform configuration
- Data persistence and customizable settings
- Secure authentication system implemented
    - [Details here](./spellbook/kotaemon/README.md)

### 12. Bolt DIY (AI Chat Interface)
- Modern AI chat interface
- Supports multiple AI providers (OpenAI, Anthropic, Google, etc.)
- Provides a Dockerized environment
- CloudFront infrastructure setup
    - [Details here](./spellbook/bolt-diy/README.md)

### 13. LLM Tester (Gradio Version)
- Gradio-based LLM proxy connection tester
- Various parameter settings and debug information display
    - [Details here](./spellbook/ee-llm-tester-gr/README.md)

### 14. LLM Tester (Streamlit Version)
- Streamlit-based LLM proxy connection tester
- Various parameter settings and debug information display
    - [Details here](./spellbook/ee-llm-tester-st/README.md)

### 15. Marp Editable UI (Markdown Presentation Editing Tool)
- Web application for creating and editing presentations in Markdown format
- Provides a Dockerized environment
    - [Details here](./spellbook/ee-marp-editable-ui/README.md)

### 16. App Gallery Showcase (Project Introduction Web Application)
- Web application for visually showcasing projects
- Provides a Dockerized environment
    - [Details here](./spellbook/app-gallery-showcase/README.md)

### 17. LibreChat (AI Chat Application)
- AI chat application supporting diverse LLM providers
- Secure authentication system and access control
    - [Details here](./spellbook/librechat/README.md)

### 18. PDF to Audio Conversion System
- System for generating audio files from PDF files
- Japanese voice conversion functionality using VOICEVOX
    - [Details here](./spellbook/pdf2audio-jp-voicevox/README.md)


## 🔧 Usage

Refer to the respective README files for instructions on using each component. For instructions on using the `amaterasu` command-line tool, refer to `spellbook/amaterasu-tool-ui/README.md`.


## 📦 Installation Instructions

1. Clone the repository.
```bash
cp .env.example .env
# Edit the .env file and make the necessary settings.
```
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```

## 🆕 What's New

This release includes the integration of LibreChat and Supabase, the introduction of a PDF to Audio conversion system, and various feature enhancements and infrastructure improvements.  Key changes include the LibreChat configuration file and documentation, the Supabase basic configuration file, the initial setup of the PDF to Audio conversion system, the addition of Terraform infrastructure configuration, and multilingual documentation support.  LiteLLM settings have also been updated, with the addition of the DeepSeek model.


## 📄 License

This project is licensed under the MIT License.