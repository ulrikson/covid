module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      width: {
        '17/24': '70.833%',
        '30/100': '30%',
        '90/100': '90%' 
      },
      colors: {
        dark: '#101821',
        semiDark: '#1a2940',
        greenBlue: 'rgba(50, 222, 212, 1)'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
