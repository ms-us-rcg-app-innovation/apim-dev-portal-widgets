# Product Build Widget

[Custom VueJS widget](./src/widget/) designed to allow the Developer/Consumer to build custom Products within the APIM instance by searching for existing canned/base Products, selecting one or more APIs, and constructing a brand new Product accessible only by said User.

See [documentation](https://learn.microsoft.com/en-us/azure/api-management/developer-portal-extend-custom-functionality#create-and-upload-custom-widget) for more details on custom widgets for the APIM Developer Portal.

## Core Prerequisites

### Install Dependencies

* Install [Node JS Runtime](https://nodejs.org/en/)
* Install [Python](https://www.python.org/downloads/) (for backend Azure Function)
* Install [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

### Provision Resources via Terraform

Use [provided Terraform resources and instructions](./infrastructure/terraform/) to provision the required Resources including APIM and an Azure Function.

### Provision Resources Manually

If not using the Terraform Infrastructure as Code, manually provision or use existing resources:

* Azure API Management instance and ensure User has Contributor permissions to said instance
* Azure Function targeting Python. 
* [Managed Identity](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp) for the Azure Function with Contributor access to the APIM instance
* Establish at least one Product with at least one API
* Establish API Tag and apply to the Product via the [az rest](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-rest) command calling the available [REST API](https://learn.microsoft.com/en-us/rest/api/apimanagement/current-ga/product-tag/assign-to-product?tabs=HTTP)

For the Azure Function, ensure the following Application Setting values are set:

* APIM_SUBSCRIPTION_ID
* APIM_RESOURCE_GROUP_NAME
* APIM_SERVICE_NAME

### Establish Environment Variables

Visit the Azure Portal to gather the following environment variable values and execute the script below.

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

### Provision Custom Widget

Log into the Azure portal with a user that has at least Contributor permissions on the APIM resource. On the APIM resource, under Developer Portal, select Portal Overview > Developer portal. This launches the Developer Portal in edit/management mode. Once in edit mode, select Custom Widgets from the side bar and follow the prompts to register a new Custom Widget. Call this widget "Product-Build". Apply this widget to a page in the Developer Portal within a full-width Section. 

For more information on establishing a new Custom Widget in the developer portal, please see the [documentation](https://learn.microsoft.com/en-us/azure/api-management/developer-portal-extend-custom-functionality#create-widget).

## Local Development

### Widget

```powershell
cd widgets/product-build/src/widget

npm install
npm start
```

Browse to the APIM Developer Portal page where the custom widget was added. Append the query string __?MS_APIM_CW_localhost_port=3000__. This should pull in the local custom widget application running on http://localhost:3000/.

NOTE: Initial setup of the custom widget requires establishing values for some required custom properties. While viewing the widget in the developer portal, click on the widget view and select __Edit Widget__. Supply values for connecting to other Azure Resources via the Custom Properties.

| Property  | Description |
| --------- | ----------- |
| Product Name Placeholder | Placeholder text in the Product Name input when creating new Product |
| Product Desc Placeholder | Placeholder text in the Product Description input when creating new Product |
| API Endpoint | API endpoint for the Azure Function app |
| Base Product Tag | API Tag name(s) of tags assigned to the base/discovery Products  |
| Enable Debug Mode | Flag to output session information to browser's console window |

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

NOTE: If troubleshooting errors related to CORS access denying requests from the APIM developer portal, take note of the source blob storage SAS domain used by the APIM developer portal to run custom widgets. Supply this unique domain as a CORS access value in the Azure Function CORS settings. Alternatively, supply "*" to allow all requests (if using the supplied Terraform scripts, set variable __cors_allow_all_origins__ to true).

### Deploy Widget Via CI/CD

Coming Soon - TODO

### Troubleshooting



### Trademarks

Trademarks This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.
