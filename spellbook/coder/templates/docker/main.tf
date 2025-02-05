terraform {
  required_providers {
    coder = {
      source = "coder/coder"
    }
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

locals {
  username = data.coder_workspace_owner.me.name
}

variable "docker_socket" {
  default     = ""
  description = "(Optional) Docker socket URI"
  type        = string
}

provider "docker" {
  # Defaulting to null if the variable is an empty string lets us have an optional variable without having to set our own default
  host = var.docker_socket != "" ? var.docker_socket : null
}

data "coder_provisioner" "me" {}
data "coder_workspace" "me" {}
data "coder_workspace_owner" "me" {}

resource "coder_agent" "main" {
  arch           = data.coder_provisioner.me.arch
  os             = "linux"
  startup_script = <<-EOT
      set -e

      # Remove symbolic link if exists
      if [ -L "/home/coder" ]; then
        sudo rm /home/coder
      fi

      # Create coder home if it doesn't exist
      if [ ! -d "/home/coder" ]; then
        sudo mkdir -p /home/coder
      fi

      # Set correct ownership
      sudo chown -R coder:coder /home

      # Copy skel files only if not initialized
      if [ ! -f /home/coder/.init_done ]; then
        cp -rT /etc/skel /home/coder
        touch /home/coder/.init_done
      fi

      # Install Python and nmon
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip nmon curl

      # Set Python3 as default python
      sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

      # Install Node.js and npm
      curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
      sudo apt-get install -y nodejs
      
      # Verify installations
      node --version
      npm --version

      # Install the latest code-server.
      # Append "--version x.x.x" to install a specific version of code-server.
      curl -fsSL https://code-server.dev/install.sh | sh -s -- --method=standalone --prefix=/tmp/code-server

      # Install VS Code extensions
      /tmp/code-server/bin/code-server --install-extension ms-python.python
      /tmp/code-server/bin/code-server --install-extension golang.go
      /tmp/code-server/bin/code-server --install-extension esbenp.prettier-vscode
      /tmp/code-server/bin/code-server --install-extension dbaeumer.vscode-eslint
      /tmp/code-server/bin/code-server --install-extension hashicorp.terraform
      /tmp/code-server/bin/code-server --install-extension redhat.vscode-yaml
      /tmp/code-server/bin/code-server --install-extension rooveterinaryinc.roo-cline
      /tmp/code-server/bin/code-server --install-extension ms-azuretools.vscode-docker
      /tmp/code-server/bin/code-server --install-extension shalldie.background
      /tmp/code-server/bin/code-server --install-extension buianhthang.gitflow
      /tmp/code-server/bin/code-server --install-extension bierner.markdown-preview-github-styles
      /tmp/code-server/bin/code-server --install-extension yzhang.markdown-all-in-one
      /tmp/code-server/bin/code-server --install-extension jock.svg
      /tmp/code-server/bin/code-server --install-extension mhutchie.git-graph
      /tmp/code-server/bin/code-server --install-extension qwtel.sqlite-viewer

      # Start code-server in the background.
      /tmp/code-server/bin/code-server --ignore-last-opened --auth none --port 13337 >/tmp/code-server.log 2>&1 &
  EOT

  # Rest of the configuration remains the same...
  env = {
    GIT_AUTHOR_NAME     = coalesce(data.coder_workspace_owner.me.full_name, data.coder_workspace_owner.me.name)
    GIT_AUTHOR_EMAIL    = "${data.coder_workspace_owner.me.email}"
    GIT_COMMITTER_NAME  = coalesce(data.coder_workspace_owner.me.full_name, data.coder_workspace_owner.me.name)
    GIT_COMMITTER_EMAIL = "${data.coder_workspace_owner.me.email}"
  }

  metadata {
    display_name = "CPU Usage"
    key          = "0_cpu_usage"
    script       = "coder stat cpu"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "RAM Usage"
    key          = "1_ram_usage"
    script       = "coder stat mem"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "Home Disk"
    key          = "3_home_disk"
    script       = "coder stat disk --path $${HOME}"
    interval     = 60
    timeout      = 1
  }

  metadata {
    display_name = "CPU Usage (Host)"
    key          = "4_cpu_usage_host"
    script       = "coder stat cpu --host"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "Memory Usage (Host)"
    key          = "5_mem_usage_host"
    script       = "coder stat mem --host"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "Load Average (Host)"
    key          = "6_load_host"
    script   = <<EOT
      echo "`cat /proc/loadavg | awk '{ print $1 }'` `nproc`" | awk '{ printf "%0.2f", $1/$2 }'
    EOT
    interval = 60
    timeout  = 1
  }

  metadata {
    display_name = "Swap Usage (Host)"
    key          = "7_swap_host"
    script       = <<EOT
      free -b | awk '/^Swap/ { printf("%.1f/%.1f", $3/1024.0/1024.0/1024.0, $2/1024.0/1024.0/1024.0) }'
    EOT
    interval     = 10
    timeout      = 1
  }
}

resource "coder_app" "code-server" {
  agent_id     = coder_agent.main.id
  slug         = "code-server"
  display_name = "code-server"
  url          = "http://localhost:13337/?folder=/home/${local.username}"
  icon         = "/icon/code.svg"
  subdomain    = false
  share        = "owner"

  healthcheck {
    url       = "http://localhost:13337/healthz"
    interval  = 5
    threshold = 6
  }
}

resource "docker_volume" "home_volume" {
  name = "coder-${data.coder_workspace.me.id}-home"
  # Protect the volume from being deleted due to changes in attributes.
  lifecycle {
    ignore_changes = all
  }
  # Add labels in Docker to keep track of orphan resources.
  labels {
    label = "coder.owner"
    value = data.coder_workspace_owner.me.name
  }
  labels {
    label = "coder.owner_id"
    value = data.coder_workspace_owner.me.id
  }
  labels {
    label = "coder.workspace_id"
    value = data.coder_workspace.me.id
  }
  # This field becomes outdated if the workspace is renamed but can
  # be useful for debugging or cleaning out dangling volumes.
  labels {
    label = "coder.workspace_name_at_creation"
    value = data.coder_workspace.me.name
  }
}

resource "docker_container" "workspace" {
  count = data.coder_workspace.me.start_count
  image = "codercom/enterprise-base:ubuntu"
  # Uses lower() to avoid Docker restriction on container names.
  name = "coder-${data.coder_workspace_owner.me.name}-${lower(data.coder_workspace.me.name)}"
  # Hostname makes the shell more user friendly: coder@my-workspace:~$
  hostname = data.coder_workspace.me.name
  # Use the docker gateway if the access URL is 127.0.0.1
  entrypoint = ["sh", "-c", replace(coder_agent.main.init_script, "/localhost|127\\.0\\.0\\.1/", "host.docker.internal")]
  env = [
    "CODER_AGENT_TOKEN=${coder_agent.main.token}",
    "USER=coder"  # coderユーザーを使用
  ]
  host {
    host = "host.docker.internal"
    ip   = "host-gateway"
  }
  volumes {
    container_path = "/home/${local.username}"
    volume_name    = docker_volume.home_volume.name
    read_only      = false
  }

  # Add labels in Docker to keep track of orphan resources.
  labels {
    label = "coder.owner"
    value = data.coder_workspace_owner.me.name
  }
  labels {
    label = "coder.owner_id"
    value = data.coder_workspace_owner.me.id
  }
  labels {
    label = "coder.workspace_id"
    value = data.coder_workspace.me.id
  }
  labels {
    label = "coder.workspace_name"
    value = data.coder_workspace.me.name
  }
}
