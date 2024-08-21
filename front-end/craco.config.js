module.exports = {
  style: {
    postcssOptions: {
      plugins: [
        require('tailwindcss')('./tailwind.config.js'),
        require('autoprefixer')
      ],
    },
  },
  eslint: null
};
