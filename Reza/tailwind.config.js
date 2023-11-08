/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        "color-primary": "#26324F",
        "color-primary-light": "#3c4761",
        "color-primary-lighter": "#515b72",
        "color-secondary": "#cae7f5",
        "color-secondary-dark": "#94c4f4",
        "color-secondary-light": "#eaf5fb",
        "color-secondary-lighter": "#f4f9fe",
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
