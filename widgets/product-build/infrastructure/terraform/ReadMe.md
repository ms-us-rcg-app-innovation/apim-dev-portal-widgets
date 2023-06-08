# Provisioning

## Bootstrap terraform by creating support infrastructure

Login to the azure cli

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

Run terraform init and specify the backend configuration. For configuration details, see the [Terraform documentation](https://developer.hashicorp.com/terraform/language/settings/backends/azurerm).

```bash
# run from terraform directory
NAME="apimwidgetproductbuild"
location="South Central US"
ARM_RESOURCE_GROUP="${NAME}-tfstate"
storage_account_name=      # tfstate resource group storage account
container_name="tfstate"
key="terraform.tfstate"
ARM_ACCESS_KEY=            # tfstate resource group storage account access key

terraform init \
-backend-config "container_name=${container_name}" \
-backend-config "key=${key}" \
-backend-config "storage_account_name=${storage_account_name}"

terraform plan
terraform apply -auto-approve
```