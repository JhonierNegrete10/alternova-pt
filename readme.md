# Junior Final

**Prueba Técnica: Desarrollador Backend - Sistema de Calificación de Notas de una Universidad**

Estás a cargo de desarrollar un sistema de calificación de notas para la Universidad Nacional. Deberás crear una API en __

**Objetivos:**

1. Implementar un sistema de autenticación utilizando Json Web Token (JWT) para usuarios, donde la encriptación del usuario y contraseña sea un requisito.
2. Crear un sistema para los alumnos que permita la gestión de materias, inscripciones, calificaciones y seguimiento del desempeño académico.

**Parte 1: Autenticación (20 puntos)**

Implementa un sistema de autenticación que cumpla con los siguientes requisitos:

- Utiliza JWT para autenticar a los usuarios.
- La encriptación del usuario y contraseña es obligatoria.

**Parte 2: Diseño de la Base de Datos (20 puntos)**

Diseña la estructura de la base de datos que incluya las entidades: Materias, Estudiantes e Inscripciones. Cada entidad debe tener los campos necesarios para almacenar la información especificada en la descripción.

Nota: Una materia tendra una o mas materias previas como requisito para poder inscrita, ej: para inscribir matematicas 2 un usuario debe haber aprobado matematicas 1 y Fisica 1

**Parte 3: Creación de la API (40 puntos)**

Diseña y documenta una API para gestionar los siguientes procesos:

1. Un estudiante se inscribe en una lista de materias.
2. Un estudiante puede obtener la lista de materias en las que está inscrito.
3. Un estudiante finaliza una materia (agrega un puntaje).
4. Un estudiante aprueba una materia con una nota igual o mayor a 3.0.
5. Un estudiante puede obtener la lista de sus materias aprobadas y su promedio de puntaje general.
6. Comprobar las materias que un estudiante ha reprobado.

**Parte 4: Documentación (10 puntos)**

Crea una documentación clara y concisa que incluya:

- Descripción de la estructura de la base de datos.
- Descripción de las rutas y endpoints de la API.
- Ejemplos de las solicitudes y respuestas de la API.
- Instrucciones para ejecutar y probar la API.

**Puntuación total: 90 puntos**

**Entrega:**

- El código de la API con las funcionalidades implementadas.
- Documentación en postman y/o swagger

Esta prueba técnica evaluará tus habilidades en autenticación, diseño de base de datos, desarrollo de API y documentación. ¡Buena suerte! 