module.exports = {
  content: ['./dist/*.html', './dist/*.js'],
  theme: {
    extend: {
      borderRadius: {
        50: '50%',
      },
      width: {
        '3/20': '15%',
        '17/20': '85%'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
