resource "azurerm_api_management" "main" {
  name                = var.apim_name
  location            = var.location
  resource_group_name = var.resource_group_name
  publisher_name      = var.publisher_name
  publisher_email     = var.publisher_email
  sku_name            = "${var.sku}_${var.sku_count}"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_application_insights" "logs" {
  name                = "${var.apim_name}-insights"
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "other"
}

resource "azurerm_api_management_logger" "example" {
  name                = "${var.apim_name}-logger"
  api_management_name = azurerm_api_management.main.name
  resource_group_name = var.resource_group_name
  resource_id         = azurerm_application_insights.example.id

  application_insights {
    instrumentation_key = azurerm_application_insights.example.instrumentation_key
  }
}