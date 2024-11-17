# modules/security/variables.tf
variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "whitelist_entries" {
  description = "List of whitelisted IPs and their descriptions"
  type = list(object({
    ip          = string
    description = string
  }))
}

variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}
