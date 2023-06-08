import { defineConfig, loadEnv } from "vite";
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const port = env.APIM_DEV_PORTAL_LOCALHOST_PORT ? parseInt(env.APIM_DEV_PORTAL_LOCALHOST_PORT) : 3000;

  return {
    plugins: [vue()],
    base: "",
    server: {
      "port": port,
      "open": `${env.APIM_DEV_PORTAL_URL}/?MS_APIM_CW_localhost_port=${port}`
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
  }
})
