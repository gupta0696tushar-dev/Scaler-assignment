/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Asana-like colors
        primary: '#3a258e',
        secondary: '#6b5ce6',
        accent: '#f06a6a',
        background: '#f5f5f5',
        surface: '#ffffff',
      },
    },
  },
  plugins: [],
}

