/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#FBF7F0",
        ink: "#2B2420",
        "ink-soft": "#6B6055",
        line: "#E2D9C8",
        surface: "#FFFFFF",
        mostaza: {
          50: "#FDF6E3", 100: "#FAE8B8", 300: "#EFC04A",
          500: "#D98E04", 600: "#B87403", 700: "#8F5A02",
        },
        brasa: { 500: "#B23A2E", 600: "#942E24" },
        oliva: { 50: "#EEF3EA", 300: "#7FA06B", 500: "#2F5233", 600: "#243F27" },
      },
      fontFamily: {
        display: ["Fraunces", "ui-serif", "Georgia", "serif"],
        body: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      boxShadow: {
        ticket: "0 1px 2px rgba(43,36,32,0.06), 0 8px 24px rgba(43,36,32,0.08)",
      },
    },
  },
  plugins: [],
}

