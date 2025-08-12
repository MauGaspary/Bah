// Para ESLint 9+, vamos usar uma configuração compatível
export default [
  {
    ignores: ['dist/**', 'node_modules/**'],
  },
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
    },
    // Usando as regras da Rocketseat de forma manual até que haja suporte completo para ESLint 9
    rules: {
      // Regras básicas que a configuração da Rocketseat normalmente aplicaria
      indent: ['error', 2],
      quotes: ['error', 'single'],
      semi: ['error', 'never'],
      'no-unused-vars': 'warn',
      'no-console': 'warn',
    },
  },
]
