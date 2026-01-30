/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/styles/**/*.css",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          400: "#d8b4fe",
          500: "#a855f7", // Required for focus:ring-primary-500
          600: "#9333ea",
          700: "#7e22ce",
          800: "#6b21a8",
        },
        dark: {
          600: "#4b5563",
          700: "#374151",
          800: "#1f2937",
          900: "#111827", // Required for focus:ring-offset-dark-900
        },
      },
    },
  },
  plugins: [],
};
