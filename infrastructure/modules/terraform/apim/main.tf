

resource "azurerm_api_management" "main" {
  name                = apim_name
  location            = azurerm_resource_group.apim_portal.location
  resource_group_name = azurerm_resource_group.apim_portal.name
  publisher_name      = var.publisher_name
  publisher_email     = var.publisher_email
  sku_name            = var.apim_sku

  identity {
    type = "SystemAssigned"
  }
}
