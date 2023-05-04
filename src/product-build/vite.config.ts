import {defineConfig} from "vite";
import vue from '@vitejs/plugin-vue';
import * as secrets from "./secrets"

// https://vitejs.dev/config/
export default defineConfig(() => ({
  plugins: [vue()],
  base: "",
  server: {
	"port": secrets.port,
	"open": `${secrets.portalUrl}/?MS_APIM_CW_localhost_port=${secrets.port}`
},
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        index: "./index.html",
        editor: "./editor.html",
      },
    },
  },
  publicDir: "static",
}))
