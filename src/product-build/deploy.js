const {deployNodeJS} = require("@azure/api-management-custom-widgets-tools")
const secrets = require("./secrets")

console.log("secrets", secrets);

const serviceInformation = {
	"resourceId": secrets.apimResourceId,
	"managementApiEndpoint": secrets.managementApiEndpoint
}
const name = "product-build"
const fallbackConfigPath = "./static/config.msapim.json"

deployNodeJS(serviceInformation, name, fallbackConfigPath)
