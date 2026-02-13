import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{vue,ts}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#fff7eb",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
          800: "#9a3412",
          900: "#7c2d12"
        },
        canvas: "#fffaf3",
        ink: "#2a1f17"
      },
      fontFamily: {
        display: ["'Manrope'", "'Segoe UI'", "sans-serif"],
        body: ["'Nunito Sans'", "'Segoe UI'", "sans-serif"]
      },
      boxShadow: {
        soft: "0 12px 24px -12px rgba(124, 45, 18, 0.35)"
      }
    },
  },
  plugins: [],
};

export default config;
