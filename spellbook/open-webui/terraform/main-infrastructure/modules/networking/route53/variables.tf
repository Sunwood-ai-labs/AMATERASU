# modules/networking/route53/variables.tf
variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "domain" {
  description = "Base domain name"
  type        = string
}

variable "subdomain" {
  description = "Subdomain prefix"
  type        = string
}


variable "alb_dns_name" {
  description = "DNS name of the ALB"
  type        = string
}

variable "alb_zone_id" {
  description = "Zone ID of the ALB"
  type        = string
}

variable "enable_health_check" {
  description = "Whether to enable Route53 health check"
  type        = bool
  default     = false
}

variable "alb_depends_on" {
  description = "Resource dependencies for the ALB record"
  type        = any
  default     = []
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "create_private_zone" {
  description = "Whether to create a private Route53 zone"
  type        = bool
  default     = false
}
