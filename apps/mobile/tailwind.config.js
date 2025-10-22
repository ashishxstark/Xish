/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: "#0A0A0A",
        neonGreen: "#1DD1A1",
        neonBlue: "#00F0FF",
      },
      fontFamily: {
        poppins: ["Poppins_400Regular", "Poppins_600SemiBold", "Poppins_700Bold"],
      },
    },
  },
  plugins: [],
};
