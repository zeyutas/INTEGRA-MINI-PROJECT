const devProxyTarget =
  process.env.VUE_APP_API_PROXY_TARGET || 'http://localhost:8000';

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: devProxyTarget,
        changeOrigin: true,
        secure: false
      }
    }
  }
};
