<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU"><img alt="GitHub Repo" src="https://img.shields.io/badge/github-AMATERASU-blue?logo=github"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases"><img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square"></a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green"></a>
</p>

<h2 align="center">Enterprise-Grade Private AI Platform (🚀 AMATERASU v1.22.0)</h2>

>[!IMPORTANT]
>This repository leverages [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage).  Approximately 90% of the release notes, README, and commit messages were generated using [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) and [claude.ai](https://claude.ai/).

>[!NOTE]
>AMATERASU is the successor project to [MOA](https://github.com/Sunwood-ai-labs/MOA).  It has evolved to run each AI service as an independent EC2 instance using Docker Compose, and deployment is simplified using Terraform.

## 🚀 Project Overview

AMATERASU is an enterprise-grade private AI platform. Built on AWS Bedrock and Google Vertex AI, it enables the development and operation of LLM-based applications in a secure and scalable environment.  Integration with GitLab streamlines version control, CI/CD pipelines, and project management. This repository serves as a "spellbook" for managing multiple AI-related projects. Each project is structured as a separate folder for deploying and managing specific AI services or functionalities.


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
- Fully automated deployment with Terraform
- Configuration management for each environment
- Version-controlled configuration

### GitLab Integration
- Improved version control, CI/CD pipelines, and project management
- Integration with self-hosted GitLab instances
- LLM-powered merge request analysis
- Automated labeling using GitLab Webhooks

### Project Exploration Functionality
- Automatic detection of Terraform projects and generation of `terraform.tfvars` files
- Simplified configuration via the `amaterasu` command-line tool


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
                GR["Gradio LLM Tester"]
                ST["Streamlit LLM Tester"]
                MEU["Marp Editable UI<br/>Presentation Editing"]
                AGS["App Gallery Showcase<br/>Project Showcase"]
            end
            
            subgraph "Fargate-based Service"
                PP["Prompt Pandora<br/>Prompt Generation Assistance"]
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
        GR --> CF
        ST --> CF
        MEU --> CF
        AGS --> CF
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
- CI pipeline and Runner configuration
- Backup and restore functionality

### 5. FG-prompt-pandora (Fargate Sample Application)
- Auto-scaling on AWS Fargate
- Prompt generation using Claude-3.5-Sonnet
- Intuitive UI based on Streamlit
    - [Details here](./spellbook/fg-prompt-pandora/README.md)

### 6. Coder (Cloud Development Environment)
- Web-based IDE
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
- Pipeline functions to enhance integration with Open WebUI
- Filter processing such as conversation turn limits and Langfuse integration
    - [Details here](./spellbook/open-webui-pipeline/README.md)

### 10. Amaterasu Tool (Terraform Variable Generator)
- Automates the generation of `terraform.tfvars` files using a command-line tool
- Generates settings for each project in the spellbook
    - [Details here](./spellbook/amaterasu-tool-ui/README.md)

### 11. Kotaemon (Document and Chat RAG UI Tool)
- RAG UI tool for document and chat interaction
- Provides Docker environment and Terraform configuration
- Data persistence and customizable settings
- Secure authentication system implemented
    - [Details here](./spellbook/kotaemon/README.md)

### 12. Bolt DIY (AI Chat Interface)
- State-of-the-art AI chat interface
- Supports multiple AI providers (OpenAI, Anthropic, Google, etc.)
- Provides a Docker containerized environment
- CloudFront infrastructure configuration
    - [Details here](./spellbook/bolt-diy/README.md)

### 13. LLM Tester (Gradio version)
- Gradio-based LLM proxy connection tester
- Various parameter settings and debug information display
    - [Details here](./spellbook/ee-llm-tester-gr/README.md)

### 14. LLM Tester (Streamlit version)
- Streamlit-based LLM proxy connection tester
- Various parameter settings and debug information display
    - [Details here](./spellbook/ee-llm-tester-st/README.md)

### 15. Marp Editable UI (Markdown Presentation Editing Tool)
- Web application for creating and editing presentations in Markdown format
- Provides a Docker containerized environment
    - [Details here](./spellbook/ee-marp-editable-ui/README.md)

### 16. App Gallery Showcase (Project Showcase Web Application)
- Web application for visually showcasing projects
- Provides a Docker containerized environment
    - [Details here](./spellbook/app-gallery-showcase/README.md)


## 🔧 Usage

Refer to the respective README files for instructions on using each component.  For instructions on using the `amaterasu` command-line tool, see `spellbook/amaterasu-tool-ui/README.md`.


## 📦 Installation Instructions

1. Clone the repository.
```bash
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git
cd AMATERASU
```
2. Follow the instructions in each project's README to install dependencies and deploy the application.
3. Enter the necessary settings in the `terraform.tfvars` file.  You can also use the `amaterasu` tool to generate this automatically.


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

Thanks to iris-s-coon and Maki for their contributions.

## 🆕 What's New

### AMATERASU v1.22.0 (Latest Release)

- **🔄 Enhanced OpenRouter API Integration**: LiteLLM's OpenRouter API integration has been enhanced and updated to the latest version.
- **🧪 Improved UI Testing Tools**: The ECS infrastructure has been optimized to an EC2 instance-based architecture, enabling more stable operation.
- **📊 Added Marp Editable UI**: A new containerized tool providing a Markdown presentation editing environment has been added.
- **🖼️ Integrated App Gallery Showcase**: A web application for beautifully showcasing projects has been added.
- **🐳 Updated Docker Images**: Several components have been updated to the latest versions, including Langfuse 3.26.
- **📐 Enhanced Architecture Visualization**: A system-wide architecture diagram has been added to clearly show the relationships between components.
- **🔍 Enhanced RAG Functionality in Open WebUI**: Added Web content loading functionality through Playwright integration.
- 🖥️ ECS task deployment has been optimized to an EC2 instance-based configuration, enabling more stable operation.
- 🔗 Docker Compose configuration improvements and standardization have strengthened inter-container collaboration.
- 🛡️ Enhanced WAF security settings and improved CSV file-based IP whitelisting management.
- 📄 Added `.env.example` files to each component for standardized and documented configuration files.
- 🧩 Improved sharing and reusability of Terraform modules.
- 🔤 Standardized environment variables to ensure consistency across different environments.


- 📝 Notes:
    - 🔄 Due to changes in LiteLLM configuration, existing configuration files need to be updated.
    - 📋 The WAF IP whitelist needs to be migrated to the new CSV format.
    - 🔍 Check the environment variable settings and update them as needed.
    - 📚 When using new components, refer to their respective READMEs for proper configuration.

This release enhances the functionality of the enterprise-grade AI platform, providing a more stable infrastructure and expanded UI tools. ✨