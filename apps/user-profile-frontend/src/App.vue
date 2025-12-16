<template>
  <div id="app">
    <div class="app-bg" />
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style scoped>
#app {
  min-height: 100vh;
  position: relative;
  color: #1f2d3d;
}

.app-bg {
  position: fixed;
  inset: 0;
  background: radial-gradient(circle at 20% 20%, rgba(64, 158, 255, 0.08), transparent 35%),
    radial-gradient(circle at 80% 10%, rgba(103, 194, 58, 0.08), transparent 30%),
    radial-gradient(circle at 30% 80%, rgba(247, 186, 42, 0.12), transparent 30%),
    linear-gradient(145deg, #f8fbff, #f2f5ff 50%, #f8fbff);
  z-index: 0;
}

.app-content {
  position: relative;
  z-index: 1;
  padding: 40px 20px 60px;
}

@media (min-width: 768px) {
  .app-content {
    padding: 60px 40px 80px;
  }
}
</style>
