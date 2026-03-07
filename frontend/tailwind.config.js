/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0070f3',
        success: '#50e3c2',
        warning: '#ff9800',
        error: '#e53935',
      }
    },
  },
  plugins: [],
}
