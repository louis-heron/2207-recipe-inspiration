import { defineConfig } from "vite"

export default defineConfig({
  build: {
    lib: {
      entry: "src/index.ts",
      formats: ["es"],
      fileName: "index",
    },
    // @streamlit/component-v2-lib is types-only at runtime — bundle everything
    rollupOptions: {
      external: [],
    },
  },
})
