# spellbook/open-webui/terraform/main-infrastructure/modules/networking/alb/variables.tf

variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "public_subnet_id" {
  description = "ID of the first public subnet"
  type        = string
}

variable "public_subnet_2_id" {
  description = "ID of the second public subnet"
  type        = string
}

variable "alb_security_group_id" {
  description = "ID of the ALB security group"
  type        = string
}

variable "certificate_arn" {
  description = "ARN of the SSL certificate"
  type        = string
}

variable "sns_topic_arn" {
  description = "ARN of the SNS topic for CloudWatch alarms"
  type        = string
}

variable "origin_secret_id" {
  description = "ID of the Secrets Manager secret containing the Origin verification header value"
  type        = string
}

variable "health_check_path" {
  description = "Path for the health check endpoint"
  type        = string
  default     = "/health"
}

variable "health_check_interval" {
  description = "Interval between health checks (in seconds)"
  type        = number
  default     = 30
}

variable "health_check_timeout" {
  description = "Timeout for health check (in seconds)"
  type        = number
  default     = 5
}

variable "health_check_healthy_threshold" {
  description = "Number of consecutive successful health checks before considering target healthy"
  type        = number
  default     = 2
}

variable "health_check_unhealthy_threshold" {
  description = "Number of consecutive failed health checks before considering target unhealthy"
  type        = number
  default     = 2
}

variable "deregistration_delay" {
  description = "Amount of time to wait before deregistering a target (in seconds)"
  type        = number
  default     = 60
}

variable "stickiness_enabled" {
  description = "Enable stickiness for the target group"
  type        = bool
  default     = true
}

variable "stickiness_duration" {
  description = "Duration for stickiness cookie (in seconds)"
  type        = number
  default     = 86400
}
