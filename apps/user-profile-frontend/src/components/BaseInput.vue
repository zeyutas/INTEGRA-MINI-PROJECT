<template>
  <div class="base-input">
    <label v-if="label" class="base-input__label">{{ label }}</label>
    <el-input
      v-bind="$attrs"
      :type="type"
      :value="value"
      :rows="rows"
      @input="$emit('input', $event)"
      @blur="$emit('blur', $event)"
    />
    <p v-if="error" class="base-input__error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'BaseInput',
  inheritAttrs: false,
  props: {
    value: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    error: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    rows: {
      type: Number,
      default: 3
    }
  }
};
</script>

<style scoped>
.base-input {
  margin-bottom: 18px;
  width: 100%;
}

.base-input__label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #596579;
}

.base-input__error {
  margin: 6px 0 0;
  color: #f56c6c;
  font-size: 12px;
}
</style>
