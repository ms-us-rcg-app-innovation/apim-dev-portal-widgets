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
    description = "The name of the app service plan."
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

variable "resource_id" {
    description = "The resource id of the resource to assign the role to."
    type        = string
}
