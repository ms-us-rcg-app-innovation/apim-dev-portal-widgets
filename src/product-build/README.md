<!-- ABOUT THE PROJECT -->
# Product Build Widget
Custom VueJS widget designed to allow the Developer/Consumer to build custom Products within the APIM instance by searching for existing canned/base Products, selecting one or more APIs, and constructing a brand new Product accessible only by said User.

See [documentation](https://learn.microsoft.com/en-us/azure/api-management/developer-portal-extend-custom-functionality#create-and-upload-custom-widget) for more details on custom widgets for the APIM Developer Portal.

## Core Prerequisites

### Establish Resources

Provision an instance of Azure API Management and ensure User has Contributor permissions on the APIM Resource. Also provision an Azure Function application targeting Python. In the APIM instance, make note of the full Resource Id, and launch the Developer Portal and make note of the URL.

TODO - provide terraform for establishing these resources.

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

# Optional variables
$env:APIM_ENDPOINT = "https://management.azure.com";
$env:APIM_DEV_PORTAL_LOCALHOST_PORT = 3000;
```

## Local Development

### Widget

```powershell
cd widget

npm install
npm start
```

### API

```powershell
cd api
py -m pip install -r requirements.txt

func start
```


## Deployment

### Deploy API Azure Function

TODO

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

TODO

### Trademarks

Trademarks This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.
