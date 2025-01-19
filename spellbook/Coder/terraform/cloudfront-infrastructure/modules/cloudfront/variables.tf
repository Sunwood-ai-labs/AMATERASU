variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "aws_region" {
  description = "AWS region for the resources"
  type        = string
  default     = "ap-northeast-1"
}

variable "origin_domain" {
  description = "Domain name of the origin (EC2 instance)"
  type        = string
}

variable "domain" {
  description = "メインドメイン名"
  type        = string
}

variable "subdomain" {
  description = "サブドメイン名"
  type        = string
}

variable "whitelist_csv_path" {
  description = "Path to the CSV file containing whitelisted IP addresses"
  type        = string
}

variable "providers" {
  description = "Required providers to be passed from root"
  type = object({
    aws           = any
    aws_virginia = any
  })
}
