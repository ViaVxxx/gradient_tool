/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
        'glass-sm': '0 2px 8px 0 rgba(31, 38, 135, 0.1)',
        'glow': '0 0 20px rgba(99, 102, 241, 0.5)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [
      {
        dark: {
          "color-scheme": "dark",
          "primary": "#e85d36",
          "primary-content": "#461e0d",
          "secondary": "#d559ce",
          "secondary-content": "#471347",
          "accent": "#b2b2ba",
          "accent-content": "#040404",
          "neutral": "#6d6593",
          "neutral-content": "#fafafc",
          "base-100": "#1b1721",
          "base-200": "#332d3d",
          "base-300": "#433c4e",
          "base-content": "#f5f4f5",
          "info": "#71a6d5",
          "info-content": "#fafcfe",
          "success": "#71c894",
          "success-content": "#fafefe",
          "warning": "#d5a559",
          "warning-content": "#fefcfa",
          "error": "#c86166",
          "error-content": "#f8f5f5",
          "--rounded-box": "1rem",
          "--rounded-btn": "2rem",
          "--rounded-badge": "1rem",
          "--animation-btn": "0.25rem",
          "--animation-input": "0.25rem",
          "--btn-focus-scale": "1",
          "--border-btn": "1.5px",
          "--tab-border": "1.5px",
          "--tab-radius": "0.5rem",
        },
      },
      "light",
    ],
    darkTheme: "dark",
    base: true,
    styled: true,
    utils: true,
    prefix: "",
    logs: true,
    themeRoot: ":root",
  },
}
