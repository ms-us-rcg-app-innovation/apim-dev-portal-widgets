const { deployNodeJS } = require("@azure/api-management-custom-widgets-tools")

const serviceInformation = {
	"resourceId": process.env.APIM_ID,
	"managementApiEndpoint": process.env.APIM_ENDPOINT,
	"tokenOverride": `Bearer ${process.env.AZ_ACCESS_TOKEN}`
}
const name = "product-build"
const fallbackConfigPath = "./static/config.msapim.json"

deployNodeJS(serviceInformation, name, fallbackConfigPath)
