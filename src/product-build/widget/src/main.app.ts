import {createApp} from "vue"
import {askForSecrets} from "@azure/api-management-custom-widgets-tools"
import App from "./components/app/index.vue"

const secretsPromise = askForSecrets("app")

const app = createApp(App).provide("secretsPromise", secretsPromise)

app.mount("#root")
