module.exports = {
  content: [
    './templates/**/*.html', // Ruta a las plantillas HTML
    './static/**/*.css',     // Ruta a los archivos CSS si usas clases personalizadas
    './**/*.py',             // Si usas clases dinámicas en los archivos Python
  ],
  theme: {
    extend: {
      colors: {
        'dark-slate-gray': '#0D1717', // Color personalizado para fondo
      },
    },
  },
  plugins: [],
};
