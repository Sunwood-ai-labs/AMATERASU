variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "whitelist_ips" {
  description = "List of IP addresses to whitelist for ingress"
  type        = list(string)
}
