terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

locals {
  suffix              = var.unique_suffix ? "-${random_string.suffix.result}" : ""
  resource_group_name = "${var.resource_group_name}${local.suffix}"
  apim_name           = "${var.apim_name}${local.suffix}"
  widget_func_name    = "${var.widget_func_name}${local.suffix}"
}

resource "random_string" "rand" {
  length  = 5
  lower   = true
  upper   = false
  numeric = false
  special = false
}

resource "azurerm_resource_group" "apim" {
  name     = local.resource_group_name
  location = var.location
}

module "apim" {
  source              = "../../../../infrastructure/terraform/modules/apim"
  apim_name           = local.apim_name
  resource_group_name = local.resource_group_name
  location            = var.location
  publisher_name      = var.publisher_name
  publisher_email     = var.publisher_email
  sku                 = var.apim_sku
  sku_count           = var.apim_sku_count
}

module "widget_func" {
  source              = "./modules/py-function"
  app_name            = local.widget_func_name
  resource_group_name = local.resource_group_name
  location            = var.location
  python_version      = "3.9"
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python"
  }
  dotnet_version               = "6.0"
  host_sku                     = "EP1"
  maximum_elastic_worker_count = 1
  elastic_instance_minimum     = 1
}
