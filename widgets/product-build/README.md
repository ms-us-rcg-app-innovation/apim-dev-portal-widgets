# Product Build Widget

[Custom VueJS widget](./src/widget/) designed to allow the Developer/Consumer to build custom Products within the APIM instance by searching for existing canned/base Products, selecting one or more APIs, and constructing a brand new Product accessible only by said User.

See [documentation](https://learn.microsoft.com/en-us/azure/api-management/developer-portal-extend-custom-functionality#create-and-upload-custom-widget) for more details on custom widgets for the APIM Developer Portal.

## Core Prerequisites

### Provision Resources

Use [provided Terraform resources and instructions](./infrastructure/terraform/) to provision the required Resources including APIM and an Azure Function.

OR 

Manually provision or use existing resources:

* Azure API Management instance and ensure User has Contributor permissions to said instance
* Azure Function targeting Python. 
* Managed Identity for the Azure Function with Contributor access to the APIM instance

### Establish Resource Prerequisites

For the APIM instance, make note of the full Resource Id under the JSON View, and launch the Developer Portal and make note of the URL. Also note the Subscription Id, Resource Group Name, and APIM name.

For the Azure Function, ensure the following Application Setting values are set:

* APIM_SUBSCRIPTION_ID
* APIM_RESOURCE_GROUP_NAME
* APIM_SERVICE_NAME

### Provision Custom Widget

Log into the Azure portal with a user that has at least Contributor permissions on the APIM resource. On the APIM resource, under Developer Portal, select Portal Overview > Developer portal. This launches the Developer Portal in edit/management mode. Once in edit mode, select Custom Widgets from the side bar and follow the prompts to register a new Custom Widget. Call this widget "Product: Build" or something similar. 

For more information on establishing a new Custom Widget in the developer portal, please see the [documentation](https://learn.microsoft.com/en-us/azure/api-management/developer-portal-extend-custom-functionality#create-widget).

### Install Dependencies

* Install [Node JS Runtime](https://nodejs.org/en/)
* Install [Python](https://www.python.org/downloads/) (for backend Azure Function)
* Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

### Establish Environment Variables

```powershell
$env:APIM_ID = "<APIM Resource Id>";
$env:APIM_DEV_PORTAL_URL = "<APIM Developer Portal Url>";
$env:APIM_SUBSCRIPTION_ID = "<APIM Subscription Id>";
$env:APIM_RESOURCE_GROUP_NAME = "<APIM Resource Group Name>";
$env:APIM_SERVICE_NAME = "<APIM Name>";

# Optional variables
$env:APIM_ENDPOINT = "https://management.azure.com";
$env:APIM_DEV_PORTAL_LOCALHOST_PORT = 3000;
```

## Local Development

### Widget

```powershell
cd widgets/product-build/src/widget

npm install
npm start
```

### API

```powershell
cd widgets/product-build/src/api
py -m pip install -r requirements.txt

func start
```

## Deployment

### Deploy API Azure Function

The [api directory](./src/api/) Azure Function runs on Python and is used for querying APIM Management utilities specifically to manage Products and APIs. See [documentation for deploying Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies).

### Deploy Widget Manually
Establish environment variables referenced above and run the following command:

```powershell
npm run deploy
```

NOTE: If troubleshooting errors related to access over port 3000, try editing the source for the @azure/api-management-custom-widget-tools via the InteractiveBrowserCredential redirectUri option in dist/index.js:

```typescript
async function getAccessToken(managementApiEndpoint) {
    const credentials = new identity.InteractiveBrowserCredential({ redirectUri: "http://localhost:3000" });
    const scope = `${managementApiEndpoint}/user_impersonation`;
    const { token } = await credentials.getToken(scope);
    return `Bearer ${token}`;
}
```
### Deploy Widget Via CI/CD

Coming Soon - TODO

### Trademarks

Trademarks This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.
