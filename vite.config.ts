import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],

  // Vite options tailored for Tauri development
  clearScreen: false,
  server: {
    port: 1420,
    strictPort: true,
    host: "localhost",
  },

  // Path aliases
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },

  // Environment prefix
  envPrefix: ["VITE_", "TAURI_"],
});
