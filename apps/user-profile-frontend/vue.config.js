const devProxyTarget =
  process.env.VUE_APP_API_PROXY_TARGET || 'http://127.0.0.1:8000';

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
