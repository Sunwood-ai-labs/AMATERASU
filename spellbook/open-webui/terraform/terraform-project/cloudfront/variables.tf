variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "Name of the project, used as a prefix for all resources"
  type        = string
}

variable "domain_name" {
  description = "Domain name for the CloudFront distribution"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
  default     = "prod"
}

variable "tags" {
  description = "Additional tags for resources"
  type        = map(string)
  default     = {}
}
