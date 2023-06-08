locals {
  # enforce storage account name restrictions:
  # * 3 - 24 characters long
  # * can only contain lowercase letters and numbers
  appstate_sa_name = substr(replace(lower(var.app_name), "/[^a-z0-9]/", ""), 0, 24)
}


# app service plan host for functions
resource "azurerm_service_plan" "host" {
  name                = var.service_plan_name
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_storage_account" "appstate" {
  name                     = local.appstate_sa_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_application_insights" "insights" {
  name                = var.app_name
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
}

resource "azurerm_linux_function_app" "func" {
  name                        = var.app_name
  resource_group_name         = var.resource_group_name
  location                    = var.location
  service_plan_id             = azurerm_service_plan.host.id
  storage_account_name        = azurerm_storage_account.appstate.name
  storage_account_access_key  = azurerm_storage_account.appstate.primary_access_key
  https_only                  = true
  functions_extension_version = "~4"

  app_settings = var.app_settings

  site_config {
    minimum_tls_version      = "1.2"
    http2_enabled            = true
    application_insights_key = azurerm_application_insights.insights.instrumentation_key
    app_scale_limit          = 5
    application_stack {
      python_version = var.python_version
    }
  }

  identity {
    type = "SystemAssigned"
  }
}

# Grant function contributor role to resource
resource "azurerm_role_assignment" "apim" {
  scope                = var.resource_id
  role_definition_name = "Contributor"
  principal_id         = azurerm_linux_function_app.func.identity[0].principal_id
}
