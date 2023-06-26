terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.0.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

data "azurerm_subscription" "current" {
}

resource "random_string" "suffix" {
  length  = 5
  special = false
  upper   = false
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
  resource_group_name = azurerm_resource_group.apim.name
  location            = var.location
  publisher_name      = var.publisher_name
  publisher_email     = var.publisher_email
  sku                 = var.apim_sku
  sku_count           = var.apim_sku_count
}

module "product" {
  source              = "./modules/apim-product-example"
  resource_group_name = azurerm_resource_group.apim.name
  apim_resource_id    = module.apim.id
  apim_name           = module.apim.name
  suffix              = "tf"
}

module "widget_func" {
  source                 = "./modules/py-function"
  app_name               = local.widget_func_name
  service_plan_name      = "${local.widget_func_name}-asp"
  resource_group_name    = azurerm_resource_group.apim.name
  location               = var.location
  python_version         = "3.9"
  cors_allow_all_origins = var.cors_allow_all_origins
  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME" = "python",
    "APIM_SUBSCRIPTION_ID"     = data.azurerm_subscription.current.subscription_id,
    "APIM_RESOURCE_GROUP_NAME" = azurerm_resource_group.apim.name,
    "APIM_SERVICE_NAME"        = module.apim.name
  }
  apim_resource_id = module.apim.id
}
