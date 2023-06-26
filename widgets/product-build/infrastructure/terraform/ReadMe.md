# Resource Provisioning Using Terraform

## Install Prerequisites

* Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
* Install [terraform](https://developer.hashicorp.com/terraform/downloads?ajs_aid=e7cb18f6-0e91-46ef-b3af-d22a83181326&product_intent=terraform)

## Bootstrap terraform by creating support infrastructure

Login to the Azure CLI

```
az login
```

Run the bootstrap terraform script. Assess and adjust any parameter values supplied to the external bootstrap module (region, name, etc.).

**NOTE: The terraform bootstrap action is a one-time execution.**

```
# run from the terraform directory
cd bootstrap
terraform init
terraform plan
terraform apply -auto-approve
```

This action will create a "tfstate" resource group with an Azure Storage Account to store the Terraform state for the application resource group. [Terraform Bootstrap module and documentation](https://github.com/ms-us-rcg-app-innovation/terraform-bootstrap). Acquire the Storage Account name and Access Key for infrasctructure commands.

## Create Azure Infrastructure

 First, define variables by creating a [terraform.tfvars](https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files) file in the terraform directory. See [variables to define](variables.tf) for details.

 Run terraform init and specify the backend configuration. For configuration details, see the [Terraform documentation](https://developer.hashicorp.com/terraform/language/settings/backends/azurerm).

```powershell
# run from terraform directory
$name="apimcw"
$env:ARM_RESOURCE_GROUP="${name}-tfstate"
$env:ARM_STORAGE_ACCOUNT_NAME=""    # tfstate resource group storage account
$env:ARM_CONTAINER_NAME="tfstate"
$env:ARM_KEY="terraform.tfstate"
$env:ARM_ACCESS_KEY=""      # tfstate resource group storage account access key

terraform init `
-backend-config "container_name=$env:ARM_CONTAINER_NAME" `
-backend-config "key=$env:ARM_KEY" `
-backend-config "storage_account_name=$env:ARM_STORAGE_ACCOUNT_NAME"

terraform plan
terraform apply -auto-approve
```