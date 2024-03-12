module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'standard',
    'react-app',
    'react-app/jest'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  plugins: [
    'react',
    'react-hooks',
    'json-format'
  ],
  rules: {
    quotes: [
      'error',
      'single'
    ],
    'jsx-quotes': [
      'error',
      'prefer-single'
    ],
    'space-before-function-paren': [
      'warn',
      'always'
    ],
    'react/prop-types': 'off'
  },
  settings: {
    'json/sort-package-json': 'standard',
    'son/ignore-files': [
      '**/package-lock.json'
    ],
    'json/json-with-comments-files': [
      '.vscode/**'
    ]
  }
}
