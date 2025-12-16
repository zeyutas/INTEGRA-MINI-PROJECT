<template>
  <div class="avatar-display">
    <el-avatar :size="size" :src="src" :alt="alt">
      {{ initials }}
    </el-avatar>
    <div class="avatar-display__meta">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AvatarDisplay',
  props: {
    src: {
      type: String,
      default: ''
    },
    alt: {
      type: String,
      default: 'Avatar'
    },
    size: {
      type: [String, Number],
      default: 96
    },
    name: {
      type: String,
      default: ''
    }
  },
  computed: {
    initials() {
      if (!this.name) return '';
      const parts = this.name.split(' ').filter(Boolean);
      return parts.map(part => part[0]).join('').toUpperCase();
    }
  }
};
</script>

<style scoped>
.avatar-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-display__meta {
  display: flex;
  flex-direction: column;
}
</style>
