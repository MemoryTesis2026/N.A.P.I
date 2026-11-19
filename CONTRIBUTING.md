# Guía de Contribución al Proyecto N.A.P.I

¡Gracias por contribuir a **N.A.P.I (ArchivaIA) · INACAP Sede Maipú**! Para mantener un desarrollo organizado, seguro y trazable, seguimos el siguiente flujo de trabajo.

---

## 1. Estrategia de Ramas (Git Flow)

El repositorio utiliza tres ramas principales protegidas:

* **`main`**: Rama de producción. Contiene únicamente código estable, probado y listo para despliegue oficial.
* **`staging`**: Rama de preproducción. Utilizada para pruebas de integración previas a un release en producción.
* **`develop`**: Rama principal de desarrollo activo. Aquí convergen las nuevas funcionalidades y correcciones antes de pasar a `staging`.

### Ramas de Trabajo (Feature / Fix branches)
* Toda nueva característica o corrección debe nacer a partir de `develop`:
  * Nuevas funciones: `feature/nombre-de-la-funcionalidad`
  * Correcciones de errores: `fix/descripcion-del-bug`
  * Mejoras de seguridad: `security/modulo-afectado`
  * Documentación: `docs/tema-documentado`

---

## 2. Convención de Mensajes de Commit

Adoptamos [Conventional Commits](https://www.conventionalcommits.org/):

* `feat:` Nuevas características en frontend o backend.
* `fix:` Correcciones de bugs o errores de ejecución.
* `security:` Mejoras en autenticación, autorización o sanitización de datos.
* `refactor:` Cambios en código que no alteran la funcionalidad externa.
* `docs:` Cambios o adiciones en documentación.
* `test:` Agregado o modificación de pruebas unitarias/integración.
* `chore:` Mantenimiento de configuración, dependencias o herramientas de CI/CD.

---

## 3. Flujo para Desarrollar y Enviar Cambios

1. **Actualizar la rama base:**
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Crear una rama para tu tarea:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

3. **Ejecutar pruebas locales y validación de código:**
   ```bash
   pytest tests/
   ruff check engine/ tests/
   ```

4. **Realizar tus commits siguiendo la convención:**
   ```bash
   git commit -m "feat(modulo): descripcion concisa del cambio"
   ```

5. **Subir tu rama y abrir un Pull Request hacia `develop`:**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```

---

## 4. Estándares de Seguridad y Privacidad

Dado que la plataforma gestiona documentos académicos y datos de usuarios (alumnos, docentes y administradores CRAI):

1. **Nunca subir secretos ni credenciales:** Las claves de Supabase, Gemini, OpenAI o Groq deben ir únicamente en variables de entorno (`.env`), el cual se encuentra ignorado en `.gitignore`.
2. **Validar permisos en servidor:** Toda operación administrativa o de modificación debe contar con validación de roles en FastAPI (`security.require_admin`, `security.require_staff`). No confiar exclusivamente en el frontend.
3. **Control estricto de archivos:** Todo documento debe pasar por validación de tamaño (máx. 100 MB), extensión y firma de bytes (magic bytes).
