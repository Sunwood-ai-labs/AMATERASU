<p align="center">
  <img src="https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/docs/amaterasu_main.png" width="100%">
  <h1 align="center">🌄 AMATERASU 🌄</h1>
</p>
<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU">
    <img alt="GitHub Repo" src="https://img.shields.io/badge/github-HarmonAI__III-blue?logo=github">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/Sunwood-ai-labs/AMATERASU?color=green">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/AMATERASU?style=social">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/releases">
    <img alt="GitHub release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/AMATERASU?include_prereleases&style=flat-square">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Sunwood-ai-labs/AMATERASU">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/pulls">
    <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/network/members">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/Sunwood-ai-labs/AMATERASU?style=social">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/AMATERASU/watchers">
    <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/Sunwood-ai-labs/AMATERASU?style=social">
  </a>
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/AMATERASU">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/AMATERASU">
</p>
<h2 align="center">
  ～ AI-Powered Automated Repository Management Template ～

<a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
<a href="https://github.com/Sunwood-ai-labs/AMATERASU/blob/main/docs/README.en.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</h2>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github" alt="GitHub">
  <img src="https://img.shields.io/badge/Actions-2088FF?style=for-the-badge&logo=github-actions" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml" alt="YAML">
  <img src="https://img.shields.io/badge/pip-3775A9?style=for-the-badge&logo=pypi" alt="pip">
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown" alt="Markdown">
  <img src="https://img.shields.io/badge/GitHub_API-181717?style=for-the-badge&logo=github" alt="GitHub API">
</p>
<p align="center">
  <a href="https://github.com/Sunwood-ai-labs/AIRA">
    <img src="https://img.shields.io/badge/AIRA-FF4500?style=for-the-badge&logo=github" alt="AIRA">
  </a>
  <a href="https://github.com/Sunwood-ai-labs/IRIS">
    <img src="https://img.shields.io/badge/IRIS-9370DB?style=for-the-badge&logo=github" alt="IRIS">
  </a>
</p>


> [!IMPORTANT]
> HarmonAI III is a template repository developed using [cline (formerly Claude Dev)](https://github.com/clinebot/cline), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), and [claude.ai](https://claude.ai/).  A large portion of the release notes, README, and commit messages were generated using the latest AI technologies.

## 🚀 Project Overview

HarmonAI III is an innovative **AI repository starter kit** integrating AIRA and IRIS. This repository aims to dramatically improve developer efficiency by providing a structure and workflow for AI development projects leveraging LLMs. Version: `v1.3.0`


## 🆕 What's New

- 🎉 **v1.3.0 Release**:  Added basic Streamlit app structure, improved README file design, fixed several bugs, and updated documentation. The Streamlit app now includes functionality to display the contents of the README.md file. Error handling for missing README.md files has also been added.  Furthermore, scripts for adding collaborators to the GitHub repository, automated synchronization workflows with Hugging Face Hub, and automated deployment workflows to PyPI have been added.


## ✨ Key Features

1. **Integrated AI Toolset**: Provides the functionality of AIRA and IRIS in a single package.
2. **Ready to Use**: Easily create a repository with a high-quality initial structure by using it as a template.
3. **Automated Development Workflow**: Automates commit message generation, release note creation, and issue management.
4. **Multilingual Support**: Supports international project deployment through automated README translation.
5. **Flexible Customization**: Easily adjustable to suit project needs.
6. **Automated Collaborator Invitation**:  Collaborator invitation script using the GitHub API.
7. **Streamlit App**: A basic Streamlit application to display the README.md file.


## 🔧 How to Use

### Running the Streamlit App
1. Install the necessary packages with: `pip install -r requirements.txt`.
2. Run: `streamlit run app.py`.

### AIRA Example:
```bash
aira --mode sourcesage commit  --config=.aira\config.dev.commit.yml --ss-model-name="gpt-4o-mini" --llm-output="llm_output.md"
```

### IRIS Example:

Refer to the documentation for each component for detailed usage instructions.


## 📦 Installation

1. Use this repository as a template to create a new repository.
2. Clone the repository locally.
3. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Customize the AIRA and IRIS configuration files.
5. Review the GitHub Actions settings and configure environment variables as needed.
6. Open the `.github/release_notes/.sourcesage_releasenotes_iris.yml` file and change the value of `repo-name:` to your new repository name.


## 🌿 Setting up the Environment

To set up the HarmonAI III environment, follow these steps:

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
   This creates a virtual environment in the `.venv` directory.

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate  # Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

These steps will prepare the development environment for HarmonAI III.


## 📚 Main Components

### 🤖 [AIRA (AI-Integrated Repository for Accelerated Development)](https://github.com/Sunwood-ai-labs/AIRA)
- Automates repository creation.
- Automates commit message generation.

### 🌈 [IRIS (Intelligent Repository Issue Solver)](https://github.com/Sunwood-ai-labs/IRIS)
- Automates issue classification.
- Automates solution suggestions.
- Automates release note generation.
- Automates README translation.

## 🤝 Automated Collaborator Invitation

HarmonAI III includes a script to automatically invite collaborators to the GitHub repository.  You can use it with the following steps:

1. Create a `.env` file and set the necessary tokens:
   ```
   # GitHub access token (for collaborator invitation)
   GITHUB_TOKEN=your_github_personal_access_token_here

   # The following are examples of tokens that may be used for other features.  It is convenient to list them for later use.
   # GITHUB_ACCESS_TOKEN=ghp_xxxxx
   # YOUR_PERSONAL_ACCESS_TOKEN_IRIS=ghp_yyyyy
   # GEMINI_API_KEY=AIzzzzz
   ```

   Note: Include the `.env` file in `.gitignore` to prevent it from being committed to the repository.

2. Run the following command to invite a collaborator:
   ```bash
   python .github/github_add_collaborator.py Sunwood-ai-labs/AMATERASU username_to_invite
   ```

   Replace `username_to_invite` with the GitHub username you want to invite.

3. Once the script runs successfully, a collaborator invitation will be sent to the specified user.

Notes:
- This script requires the GitHub token to have appropriate permissions (the `repo` scope).
- When used for an organization's repository, ensure that appropriate permissions are granted in the organization's settings.
- For security, update the token regularly and grant only the minimum necessary permissions.
- Never commit information including the `.env` file or tokens to a public repository.

This feature simplifies the process of adding new contributors to the project.  It allows for efficient team expansion while maintaining security.

## 🐈 Process Flow


```mermaid
%%{init:{'theme':'base','themeVariables':{'primaryColor':'#024959','primaryTextColor':'#F2C335','primaryBorderColor':'#F2AE30','lineColor':'#A1A2A6','secondaryColor':'#593E25','tertiaryColor':'#F2C335','noteTextColor':'#024959','noteBkgColor':'#F2C335','textColor':'#024959','fontSize':'18px'}}}%%

graph LR
    A[Start] --> B[Repository Conception and Naming]
    B -->|Human Action| C[HarmonAI III Repository Initialization]
    C -->|Automated| D[Development Work]
    D -->|Human Action| E[AIRA Commit Automation]
    E --> H[IRIS Release Note Creation]
    H --> I[IRIS Documentation Translation]
    I --> J[Release]
    J --> K[End]

    class B,D,G human;
    class E aira;
    class F,H,I iris;
    class C auto;
    class A,J,K process;

```



## 🤝 Contributing

HarmonAI III welcomes contributions from the community as an open-source project.  Please help improve this template repository through bug reports, feature requests, and pull requests.

## 📄 License

HarmonAI III is released under the [MIT License](LICENSE).

## 🙏 Acknowledgements

HarmonAI III has drawn inspiration from many open-source projects during its development.  We especially thank the developers of AIRA and IRIS.  We also thank iris-s-coon and Maki.

---

HarmonAI III is an excellent starter kit for realizing AI-driven development processes. Let's start developing innovative AI projects based on this template!