variable "apim_resource_id" {
  description = "The resource id of the APIM resource."
  type        = string
}

variable "apim_name" {
  description = "The name of the APIM resource."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}

variable "base_product_tag_name" {
  description = "The name of the API Tag that will be applied to base products."
  type        = string
  default     = "base-product"
}

variable "suffix" {
  description = "Optional suffix to apply to all namings."
  type        = string
  default     = ""
}


