variable "unique_suffix" {
  description = "A suffix to append to the names of all resources."
  type        = bool
  default     = true
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the resources."
  type        = string
}

variable "location" {
  description = "The location/region where the resources should be created."
  type        = string
  default     = "South Central US"
}

variable "publisher_name" {
  description = "The name of your organization for use in the developer portal and e-mail notifications."
  type        = string
}

variable "publisher_email" {
  description = "The e-mail address to receive all system notifications."
  type        = string
}

variable "apim_sku" {
  description = "The pricing tier of this API Management service"
  default     = "Developer"
  type        = string
  validation {
    condition     = contains(["Developer", "Standard", "Premium"], var.apim_sku)
    error_message = "The apim_sku must be one of the following: Developer, Standard, Premium."
  }
}
variable "apim_sku_count" {
  description = "The instance size of this API Management service."
  default     = 1
  type        = number
  validation {
    condition     = contains([1, 2], var.apim_sku_count)
    error_message = "The apim_sku_count must be one of the following: 1, 2."
  }
}

variable "widget_func_name" {
  description = "The name of the function app."
  type        = string
}

variable "apim_name" {
  description = "The name of the API Management service."
  type        = string
}

variable "base_product_tag_name" {
  description = "The name of the API Tag that will be applied to base products."
  type        = string
  default     = "base-product"
}

variable "cors_allow_all_origins" {
  description = "Whether to allow all origins for CORS."
  type        = bool
  default     = false
}

