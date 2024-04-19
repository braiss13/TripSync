# Links management web

## Intro

Una web de demostración sobre el manejo de enlaces url creada con Flask.

<i>A demo web for managing url links created with Flask.</i>

## Build

Solo tienes que instalar **Flask** y algunas dependencias y ejecutar `app.py`.

<i>Just install **Flask** and some dependencies and execute `app.py`.</i>

```bash
$ pip install -U -r requirements.txt
$ python app.py
```

El proyecto fue creado con **PyCharm**, pero puede utilizarse cualquier otro IDE.

<i>The project was created with **PyCharm**, but you can use any IDE you need.</i>

## Deploy

Al ejecutarse, el programa generará una excepción debido a que no será capaz de enontrar el archivo de configuración `instance/config.json`. Esto es debido a que en este archivo se guarda la clave secreta de la app, y por ello no tiene sentido distribuirla.

Será necesario proporcionar un archivo `instance/config.json` con el contenido de la `SECRET_KEY', por ejemplo:

```json
{
  "SECRET_KEY"="Lalala"
}
```
