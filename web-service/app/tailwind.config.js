module.exports = {
  content: ['./{pages,components,layouts,plugins}/**/*.{vue,js,ts}'],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: false,
  },
  plugins: [require('daisyui')],
}
