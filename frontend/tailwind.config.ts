import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{vue,ts}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "var(--brand-50)",
          100: "var(--brand-100)",
          200: "var(--brand-200)",
          300: "var(--brand-300)",
          400: "var(--brand-400)",
          500: "var(--brand-500)",
          600: "var(--brand-600)",
          700: "var(--brand-700)",
          800: "var(--brand-800)",
          900: "var(--brand-900)"
        },
        canvas: "var(--color-bg)",
        ink: "var(--color-text-dark)",
        primary: "var(--color-primary)",
        "primary-dark": "var(--color-primary-dark)",
        accent: "var(--color-accent)",
        surface: "var(--color-surface)",
        muted: "var(--color-text-muted)"
      },
      fontFamily: {
        display: ["'Playfair Display'", "'Cormorant Garamond'", "serif"],
        body: ["'Cormorant Garamond'", "'Playfair Display'", "serif"],
        script: ["'Dancing Script'", "cursive"]
      },
      boxShadow: {
        soft: "var(--shadow-soft)",
        card: "var(--shadow-card-hover)"
      },
      backgroundImage: {
        "brand-gradient": "linear-gradient(135deg, var(--color-primary), var(--color-accent))"
      }
    },
  },
  plugins: [],
};

export default config;

