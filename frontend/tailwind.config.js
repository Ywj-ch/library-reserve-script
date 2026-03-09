/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6366F1',
        secondary: '#818CF8',
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
      }
    },
  },
  plugins: [],
}
