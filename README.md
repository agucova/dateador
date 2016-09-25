hu# Dateador
Script que se conecta a dos sitios diferentes para obtener información de personas chilenas.
<pre>
╔═══╗  ╔╗        ╔╗
╚╗╔╗║ ╔╝╚╗       ║║
 ║║║╠═╩╗╔╬══╦══╦═╝╠══╦═╗
 ║║║║╔╗║║║║═╣╔╗║╔╗║╔╗║╔╝
╔╝╚╝║╔╗║╚╣║═╣╔╗║╚╝║╚╝║║
╚═══╩╝╚╩═╩══╩╝╚╩══╩══╩╝
</pre>
# Requisitos
Antes de usarlo, necesitarás las siguientes dependencias:
- Python 2.7
- BeautifulSoup (`pip install beautifulsoup`)
- Requests (`pip install requests`)
- TermColor (`pip install termcolor`)
- HTML5Lib (`pip install --upgrade html5lib==1.0b8`)
# Uso
Hay 2 modos de uso, interactivo y por argumentos.
## Ejemplos
### Interactivo
```shell
# Al no darse argumentos, se usa el modo interactivo
python dateador.py
```
### Con Argumentos

```shell
# El nombre se da directamente desde la cli.
python dateador.py -n Pedro Aguirre
```
```shell
# Con modo stalker, que da una lista de coincidencias.
python dateador.py -s -n Pedro Aguirre
```
```shell
# Guarda la información recolectada en un archivo.
python dateador.py -n Pedro Aguirre -o log.txt
```
