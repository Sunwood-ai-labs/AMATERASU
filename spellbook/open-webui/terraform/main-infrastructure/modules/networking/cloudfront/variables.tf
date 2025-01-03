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

variable "route53_zone_id" {
  description = "ID of the Route53 hosted zone"
  type        = string
}

variable "existing_record_id" {
  description = "ID of the existing Route53 A record"
  type        = string
  default     = ""  # デフォルト値を空文字列に設定
}

variable "wait_for_existing_record" {
  description = "Whether to wait for the existing record to be created"
  type        = bool
  default     = true
}
