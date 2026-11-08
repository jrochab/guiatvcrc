# Guía de TV: piloto experimental

## Qué contiene
Web móvil, siete canales configurados, extractor experimental y flujo de GitHub Actions para actualizar y publicar en GitHub Pages. No requiere contraseñas en el código. Se eligió una sola plataforma para simplificar el piloto; Cloudflare no es necesario para esta versión.

## Importante antes de empezar
El código se generó sin acceso de red a las fuentes desde el entorno de ejecución. No se ha validado la extracción real ni se ha desplegado. El extractor busca tablas HTML con horas; puede devolver cero programas o requerir cambios por canal. Ningún resultado se considera verificado automáticamente. No hay conversión horaria ni vista fiable de ahora/después todavía. No se suministran datos de ejemplo como si fueran actuales.

Revise términos de uso y permisos de la fuente antes de activar consultas periódicas. No eluda bloqueos, autenticación ni medidas antiautomatización. Para un servicio público, confirme el permiso para reutilizar la programación.

## Publicar desde el celular
1. Abra GitHub en el navegador. Si la interfaz no muestra todas las opciones, use «Sitio de escritorio».
2. Cree un repositorio nuevo para el piloto. El uso público requiere revisar previamente los permisos de los datos. Revise también los límites y condiciones de su plan.
3. Descomprima el ZIP. Suba el CONTENIDO de la carpeta del proyecto, conservando los subdirectorios. GitHub no descomprime automáticamente un ZIP subido.
4. Verifique que existen channels.json, requirements.txt, scripts/update.py, site/index.html y .github/workflows/update.yml en sus rutas exactas. Algunos gestores ocultan .github por empezar con punto; el flujo también se entrega como PLANTILLA_FLUJO.txt para copiarlo manualmente si hace falta.
5. En el repositorio abra Settings > Pages y seleccione GitHub Actions como origen cuando la interfaz lo permita.
6. Abra Actions > Actualizar y publicar guía > Run workflow.
7. Espere a que termine. La ejecución de publicación mostrará la dirección de la web.
8. Compruebe los resultados de cada canal contra la fuente; que el flujo termine bien NO demuestra que la parrilla sea correcta.

## Automatización
El flujo solicita actualizaciones dos veces al día, a las 10:17 y 22:17 UTC. Son 04:17 y 16:17 en Costa Rica. Los horarios de ejecución no son garantía de puntualidad; los límites y la inactividad del repositorio pueden afectar las tareas. Se puede lanzar Run workflow manualmente. No hace falta dejar el teléfono encendido.

No se conservan parrillas anteriores en este piloto: si una fuente falla se muestra el error, no datos viejos como actuales.

## Diagnóstico
- «Sin programación recuperada»: revise si el HTML contiene tablas de horarios y adapte scripts/update.py. El script no ejecuta JavaScript.
- Horas incorrectas: compruebe la señal y zona horaria. timezone es informativo y no convierte nada en esta versión.
- Fecha: se solicita /AAAA-MM-DD. Esa dirección sola no prueba que la fuente entregue ese día; revise el encabezado y los programas.
- Fallo de descarga: examine la ejecución de Actions. No aumente agresivamente la frecuencia ni intente sortear bloqueos.
- Fallo de Pages: compruebe permisos y configuración del repositorio.

## Modificar canales
Edite channels.json, manteniendo id, name y url. Las señales configuradas son las siete que solicitó Jimmy. Nunca sustituya una señal por la de otro país sin validarla.

## Prueba local opcional
Instale Python 3.12, ejecute `pip install -r requirements.txt`, luego `python scripts/update.py`. Para ver la web use `python -m http.server 8000 --directory site` y abra localhost:8000. No abra index.html directamente porque el navegador puede bloquear la carga de data.json.

## Pendientes para una versión estable
Validar selectores y fechas por canal, identificar zonas horarias, comprobar cada señal, permisos de reutilización, conservar último dato válido con aviso de antigüedad y agregar ahora/después tras validar esas bases.
