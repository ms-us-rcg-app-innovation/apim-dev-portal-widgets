variable "service_plan_name" {
  description = "The name of the app service plan."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the app service plan."
  type        = string
}

variable "location" {
  description = "The location/region where the app service plan should be created."
  type        = string
}

variable "app_name" {
  description = "The name of the application."
  type        = string
}

variable "app_settings" {
  description = "The app settings to use for the app service plan."
  type        = map(string)
}

variable "python_version" {
  description = "The python version to use for the app service plan."
  type        = string
}

variable "apim_resource_id" {
  description = "The resource id of the APIM resource."
  type        = string
}

variable "cors_allow_all_origins" {
  description = "Whether to allow all origins for CORS."
  type        = bool
  default     = false
}

