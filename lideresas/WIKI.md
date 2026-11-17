# WIKi LIDERESAS

## Cosas que necesitas saber

- Aplicacion escrita en python, utiliza django y tailwind.

- para la base de datos utiliza mysql. esto porque se monto en un cpanel de hosting.

- sistemas de cache, tiene 2 sistemas de cache. una en memoria y otra en disco por achivos. no lo parece pero el sistema por archivos es mas rapido que el sistema en memoria.

- existes unos snippets para html y para python. los de python bien usados, te permiten ahorrar mucho tiempo.

- los archivos estatisticos de la aplicacion estan en la carpeta de la aplicacion. y son servidos por whitenoise.

- la aplicacion esta en el estandar wsgi. y no en asgi. esto quiere decir que. cuando se ejecuta la aplicacion, se ejecuta en un servidor wsgi. con varios procesos/threads.

- cuando montes la aplicacion tienes que setear unas variables de entorno. y no se pueden cambiar en el servidor.
    - DJANGO_SECRET_KEY
    - DJANGO_ALLOWED_HOSTS
    - DJANGO_DEBUG
    - DATABASE_URL

- la aplicacion tiene un sistema de logs.

## Donde Buscar Información
- [x] Documentación de la aplicación, revisa los archivos, cada modelo, cada vista, cada formulario, cada filtro, cada función, etc. tiene su documentación.

- [x] Documentacion de django. revisa la documentación de django la oficial. [url](https://docs.djangoproject.com/en/5.2/)

- [x] Documentacion de tailwind. para manejar los estilos de la aplicación. revisa la documentación de tailwind la oficial. [url](https://tailwindcss.com/docs/styling-with-utility-classes)

- [x] Documentacion de django filters. para manejar los filtros de la aplicación. [url](https://django-filter.readthedocs.io/en/stable/guide/usage.html)

- [x] Documentacion de django-tailwind. es lo que permite usar tailwind con django. [url](https://django-tailwind.readthedocs.io/en/latest/)

- [x] Django Cookiecutter. Fue la herramienta con la que se inicializo la aplicación. [url](https://github.com/pydanny/cookiecutter-django), esta fue muy modificada por el proyecto. 

## Cosa que hacer

- Manten el estilo de codigo de la aplicación, guiate por el código de la aplicación y revisa los estilos de la aplicación.

- Manten la nomenclatura de la aplicación, los modelos, los formularios, los filtros, etc. estan en ingles y con un sistema de nomenclatura estandarizado. es por tu bien.

- Instala las extensiones recomendadas, junto a las librerias de desarrollo de la aplicación. te facilita la vida. te ayudaran a mantener la aplicación. 


## Cosa que no hacer

- No añadas librerias a la aplicación por añadirlas, lo mas seguro no las necesites. la mayoria de problemas fueron resueltos.

- No borres la documentación de la aplicación, vas a perder la información que necesitas. 

- No cambies el nombre de los modelos, los formularios, los filtros, etc. romperas mas de alguna cosa.

- No cambies la visibilidad del repositorio a publico, no es necesario.

## contacto

### email
diego.rivera.estefano@gmail.com

### discord: 
vadnir#1298

