Este repositorio forma parte del Proyecto final de un master en python. Esta desarrollado con Python como lenguaje de programacion para el backend, Django como framework y html y css para el frontend.

El proyecto simula una Plataforma de contenidos audiovisuales, con gestion de usuarios, de peliculas y series del lado del administrador y una gestion de peliculas o series favoritas y vistas 
(tanto peliculas como series) del lado del usuario registrado.

incluye tambien gestion de estadisticas del lado del administrador (ver estadisticas generales de toda la plataforma, y estadisticas particulares de cada usuario), 
del lado del usuario registrado este tambien podra tener acceso a sus propias estadisticas, tales como: 
Peliculas vistas, series vistas, minutos totales  usados en ver peliculas o series y estadisticas de distribucion de generso vistos tanto en peliculas como series.

La plataforma ( que he llamado MiFlix) incluye tambien un buscador para poder buscar una serie o pelicula determinada y ver su detalle.

Un usuario no registrrado podra navegar por la web viendo el contenido pero no podra interactuar con el. Podra ver las peliculas o series del catalogo y acceder al detalle de cada pelicula o serie que quiera o usar el buscador para buscar contenido, pero nada mas.

Un usuario registrado ademas de todo lo anterior podra ver ademas en el detalle de cada pelicula o serie a la que acceda un boton para agregarlas a sus "favoritos" y otro para agregarlas a "ya vistas", ademas de poder ver sus estadisticas personales de uso de la plataforma.

Un usuario administrador ademas de todo lo anterior, tendra un panel de administracion desde donde poder gestionar usuarios, contenidos y ver estadisticas. Desde ese panel, podra Crear, editar, eliminar o consultar un usuario y hacer lo mismo con las peliculas y series.

Se ha creado un panel de administracion dentro de la propia web para que no tenga que  gestionar nada desde la parte del admin de la base de datos.
La base de datos esta hecha con Sqlite3.

Como IDE se ha utilizado Pycharm en su version gratuita.
