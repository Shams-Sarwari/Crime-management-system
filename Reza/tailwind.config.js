/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.{html,js}", "../**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#26324F",
        "color-primary-light": "#3c4761",
        "color-primary-lighter": "#515b72",
      },
      fontFamily: {
        salamat: ["A Salamat", "sans-serif"],
        IRANSans: ["IRANSans", "sans-serif"],
        baseet: ["Far.Baseet", "IRANSans"],
        kamran: ["Far.Kamran", "IRANSans"],
        roya: ["Far.Roya", "IRANSans"],
      },
    },
  },
  plugins: [],
};
