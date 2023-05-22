<!-- ABOUT THE PROJECT -->
# Product Build Widget
Custom VueJS widget designed to allow the Developer/Consumer to build custom Products within the APIM instance by searching for existing canned/base Products, selecting one or more APIs, and constructing a brand new Product accessible only by said User.

See [documentation](https://learn.microsoft.com/en-us/azure/api-management/developer-portal-extend-custom-functionality#create-and-upload-custom-widget) for more details on custom widgets for the APIM Developer Portal.

## Core Prerequisites

### Install Dependencies

* Install [Node JS Runtime](https://nodejs.org/en/)
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

```powershell
npm install
npm start
```

## Deployment

### Deploy Manually
Establish environment variables referenced above and run the following command:

```powershell
npm run deploy
```

NOTE: If troubleshooting errors related to access over port 3000, try editing the source for the @azure/api-management-custom-widget-tools via the InteractiveBrowserCredential redirectUri option in dist/index.js.

```typescript
async function getAccessToken(managementApiEndpoint) {
    const credentials = new identity.InteractiveBrowserCredential({ redirectUri: "http://localhost:3000" });
    const scope = `${managementApiEndpoint}/user_impersonation`;
    const { token } = await credentials.getToken(scope);
    return `Bearer ${token}`;
}
```
### Deploy Via CI/CD

TODO

### Trademarks

Trademarks This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.
