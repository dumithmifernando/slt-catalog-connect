import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // so the frontend can just call fetch("/api/...") in dev
      "/api": "http://localhost:5000",
    },
  },
});
