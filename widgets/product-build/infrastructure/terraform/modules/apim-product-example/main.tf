locals {
  suffix = length(var.suffix) > 0 ? "-${var.suffix}" : ""
}

resource "azurerm_api_management_api" "api1" {
  name                = "example-api-1${local.suffix}"
  resource_group_name = var.resource_group_name
  api_management_name = var.apim_name
  revision            = "1"
  display_name        = "Example API 1${local.suffix}"
  path                = "example-1${local.suffix}"
  protocols           = ["https"]
}

resource "azurerm_api_management_api" "api2" {
  name                = "example-api-2${local.suffix}"
  resource_group_name = var.resource_group_name
  api_management_name = var.apim_name
  revision            = "1"
  display_name        = "Example API 2${local.suffix}"
  path                = "example-2${local.suffix}"
  protocols           = ["https"]
}

resource "azurerm_api_management_api" "api3" {
  name                = "example-api-3${local.suffix}"
  resource_group_name = var.resource_group_name
  api_management_name = var.apim_name
  revision            = "1"
  display_name        = "Example API 3${local.suffix}"
  path                = "example-3${local.suffix}"
  protocols           = ["https"]
}

resource "azurerm_api_management_product" "baseproduct" {
  product_id            = "base-product${local.suffix}"
  api_management_name   = var.apim_name
  resource_group_name   = var.resource_group_name
  display_name          = "Base Product${local.suffix}"
  subscription_required = true
  approval_required     = false
  published             = false
}

resource "azurerm_api_management_product_api" "api1" {
  api_name            = azurerm_api_management_api.api1.name
  product_id          = azurerm_api_management_product.baseproduct.product_id
  api_management_name = var.apim_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_api_management_product_api" "api2" {
  api_name            = azurerm_api_management_api.api2.name
  product_id          = azurerm_api_management_product.baseproduct.product_id
  api_management_name = var.apim_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_api_management_product_api" "api3" {
  api_name            = azurerm_api_management_api.api3.name
  product_id          = azurerm_api_management_product.baseproduct.product_id
  api_management_name = var.apim_name
  resource_group_name = var.resource_group_name
}

resource "azurerm_api_management_tag" "baseproducttag" {
  api_management_id = var.apim_resource_id
  name              = var.base_product_tag_name
}

resource "azurerm_api_management_product_tag" "baseproducttag" {
  api_management_product_id = azurerm_api_management_product.baseproduct.product_id
  api_management_name       = var.apim_name
  resource_group_name       = var.resource_group_name
  name                      = azurerm_api_management_tag.baseproducttag.name
}