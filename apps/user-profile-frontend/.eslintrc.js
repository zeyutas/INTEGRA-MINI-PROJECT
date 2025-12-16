module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/essential'
  ],
  parserOptions: {
    parser: 'babel-eslint'
  },
  rules: {
    semi: 'off',
    'space-before-function-paren': 'off',
    'spaced-comment': 'off',
    'no-multiple-empty-lines': 'off'
  }
};
