module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://10.0.0.171:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
};
