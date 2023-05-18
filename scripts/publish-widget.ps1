# get the directory of script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition

# find parent directory of script directory
$rootPath = Split-Path -Parent $scriptPath

# push to root directory
Push-Location $rootPath

# change to the terraform infrastructure directory
$infraPath = Join-Path -Path $rootPath -ChildPath "infrastructure"

# push infra path directory to the directory stack
Push-Location $infraPath

# execute tarraform steps
terraform init
terraform plan -out=apim.tfplan -var-file=apim.tfvars
terraform apply apim.tfplan

# capture output variables
$terraformOut = terraform output -json | ConvertFrom-Json

# set env. vars needed for widget build
$env:APIM_ID = $terraformOut.apim_id.value
$env:APIM_ENDPOINT = $terraformOut.apim_endpoint.value

# get access token to APIM instance
$token = az account get-access-token --resource=https://management.azure.com/ | ConvertFrom-Json

$env:AZ_ACCESS_TOKEN = $token.accessToken

# pop the infra directory from the directory stack
Pop-Location

# create the path to the widget directory
$widgetPath = Join-Path -Path $rootPath -ChildPath "src/product-build"

# push the widget directory to the directory stack
Push-Location $widgetPath

# install npm dependencies
npm install

# run deployment script
npm run deploy