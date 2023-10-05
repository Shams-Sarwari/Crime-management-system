/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#26324F",
        "color-primary-light": "#3c4761",
        "color-primary-lighter": "#515b72",
      },
    },
  },
  plugins: [],
};
