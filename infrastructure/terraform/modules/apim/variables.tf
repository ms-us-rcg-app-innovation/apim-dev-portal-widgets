variable "apim_name" {
  description = "The name of the API Management service."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group in which to create the API Management service."
  type        = string
}

variable "location" {
  description = "The location/region where the API Management service should be created."
  type        = string
}

variable "publisher_name" {
  description = "The name of your organization for use in the developer portal and e-mail notifications."
  type        = string
}

variable "publisher_email" {
  description = "The e-mail address to receive all system notifications."
  type        = string
}

variable "sku" {
  description = "The pricing tier of this API Management service"
  default     = "Developer"
  type        = string
  validation {
    condition     = contains(["Developer", "Standard", "Premium"], var.sku)
    error_message = "The sku must be one of the following: Developer, Standard, Premium."
  }
}

variable "sku_count" {
  description = "The instance size of this API Management service."
  default     = 1
  type        = number
  validation {
    condition     = contains([1, 2], var.sku_count)
    error_message = "The sku_count must be one of the following: 1, 2."
  }
}