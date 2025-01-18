module.exports = {
  content: [
    './templates/**/*.html',          // Plantillas HTML principales
    './static/**/*.css',             // Archivos CSS personalizados
    './**/*.py',                     // Archivos Python que usan clases dinámicas
    './MiFlixApp/templates/**/*.html', // Plantillas de MiFlixApp
    './usuarios/templates/**/*.html',   // Plantillas de usuarios
  ],
  theme: {
    extend: {
      screens: {
        'xs': '480px',    // Teléfonos pequeños
        'sm': '640px',    // Teléfonos estándar
        'md': '768px',    // Tablets
        'lg': '1024px',   // Laptops
        'xl': '1280px',   // Pantallas grandes
        '2xl': '1536px',  // Pantallas extra grandes
      },
      colors: {
        'dark-slate-gray': '#0D1717', // Color personalizado para fondo
        'soft-pink': '#ffafcc',       // Ejemplo de color adicional
        'light-gray': '#f5f5f5',     // Color claro para fondos secundarios
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
      },
      borderRadius: {
        'xl': '1.5rem', // Bordes redondeados personalizados
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'), // Mejora estilos de texto
    require('@tailwindcss/forms'),      // Mejora formularios
    require('@tailwindcss/aspect-ratio'), // Controla proporciones de imágenes y videos
  ],
};
