#!/usr/bin/python
#-*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import httplib
import urllib
from termcolor import colored
import json
from datetime import datetime
import sys
import argparse

# Argumentos!


class CapitalisedHelpFormatter(argparse.HelpFormatter):

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Uso: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)
parser = argparse.ArgumentParser(
    description='Búsqueda de información en dbs chilenas.', add_help=False, formatter_class=CapitalisedHelpFormatter)
parser._optionals.title = 'Argumentos Opcionales:'
parser.add_argument('-s', '--stalker', action='store_true',
                    help='Modo stalker, lista de coincidencias.')
parser.add_argument('-o', '--output', nargs='?', metavar='archivo',
                    help='Elegir un archivo para guardar un log.')
parser.add_argument('-n', '--nombre', nargs='*',
                    metavar='búsqueda', help='Nombre a ser buscado.')
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='Muestra este mensaje de ayuda y sale.')
args = parser.parse_args()
# definimos la hora
fecha = datetime.now()
hora = '%s/%s/%s a las %s:%s:%s' % (fecha.day, fecha.month,
                                    fecha.year, fecha.hour, fecha.minute, fecha.second)

# Mensaje de inicio
print colored("""
                   ╔═══╗  ╔╗        ╔╗
                   ╚╗╔╗║ ╔╝╚╗       ║║
                    ║║║╠═╩╗╔╬══╦══╦═╝╠══╦═╗
                    ║║║║╔╗║║║║═╣╔╗║╔╗║╔╗║╔╝
                   ╔╝╚╝║╔╗║╚╣║═╣╔╗║╚╝║╚╝║║
                   ╚═══╩╝╚╩═╩══╩╝╚╩══╩══╩╝
                      v1.0 by @unkndown
""", "blue", attrs=['bold'])
# opciones
print colored(" Obtén los datos de una persona con el rut o nombre de ella: \n\n -Ejemplo con rut: 5519653-2 \n -Ejemplo con nombre: Pedro Aguilar Toloza\n -Si tienes solo una parte del nombre, usa la opcion stalker\n", "magenta", attrs=['bold'])
# Iniciamos la ejecucion
try:

    #
    # Obtenemos el rut a partir del dato que nos de el usuario
    #
    if args.nombre is None:
        nombre = raw_input("Ingresa un rut o nombre: ")
    else:
        nombre = " ".join(args.nombre)
    print colored(" \n [+] Buscando datos \n", "green", attrs=['bold'])
    link = "http://chile.rutificador.com/get_generic_ajax/"
    host = "chile.rutificador.com:80"
    parametros = urllib.urlencode(
        {'csrfmiddlewaretoken': '2', 'entrada': nombre})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain", "Cookie": "csrftoken=2"}
    conexion = httplib.HTTPConnection(host)
    conexion.request("POST", link, parametros, headers)
    respuesta = conexion.getresponse()
    ver_source = respuesta.read()
    data = json.loads(ver_source)

    # verificamos si se ha encontrado un dato
    if data['status'] != "not_found":
        # verificamos si se ha pasado un parametro
        if args.stalker:
            print colored("+------------------------------------------+", "green", attrs=['bold'])
            # contamos los registros encontrados
            total = len(data['value'])
            # abrimos el archivo datos.txt o lo creamos si no existe para
            # guardar el resultado de la busqueda
            datos = ""
            datos += "+------------------------------------------+\n"
            # mostramos la fecha de la busqueda
            datos += "         " + hora + "\n"
            datos += "+------------------------------------------+\n"
            # mostramos los datos encontrados
            for i in range(1, total):
                nombre = data['value'][i]['name']
                rut = str(data['value'][i]['rut']) + \
                    "-" + str(data['value'][i]['dv'])
                datos += u' - '.join((nombre, rut)
                                     ).encode('utf-8').strip() + "\n"
                print colored(" Nombre: ", "blue", attrs=['bold']) + nombre + "\n" + colored(" Rut: ", "blue", attrs=['bold']) + rut
                print colored("+------------------------------------------+", "green", attrs=['bold'])
            # guardamos los datos en el archivo txt
            if args.output is not None:
                txt = open(args.output, 'a')
                txt.write(datos)
                txt.close()
                exit()

        # definimos el rut
        rut = str(data['value'][0]['rut']) + str(data['value'][0]['dv'])
        print colored("+------------------------------------------+", "green", attrs=['bold'])
        print colored(" Rut: ", "blue", attrs=['bold']) + rut

        #
        # Obtenemos la informacion a partir del rut obtenido
        #

        url = "http://buscardatos.com/cl/personas/padron_cedula_chile.php"
        hosts = "buscardatos.com:80"
        post = urllib.urlencode({'cedula': rut})
        conex = httplib.HTTPConnection(hosts)
        conex.request("POST", url, post, headers)
        request = conex.getresponse()

        # verificamos si el status de nuestra peticion es 200
        if request.status == 200:
            respuesta = request.read()
            html = BeautifulSoup(respuesta, "html5lib")
            entradas = html.find_all('tr')
            datos = ""
            datos += "+------------------------------------------+\n"
            datos += "         " + hora + "\n"
            datos += "+------------------------------------------+\n"

            # mostramos la información
            for item in entradas:
                item.encode('utf-8')
                resultado = item.getText()
                reemplazar = resultado.replace(">", "")
                separar = reemplazar.split(":", 1)
                datos += u' '.join((' ', reemplazar)
                                   ).encode('utf-8').strip() + "\n"
                print colored("+------------------------------------------+", "green", attrs=['bold'])
                print str(" ") + colored(separar[0], "blue", attrs=['bold']) + str(":") + separar[1]
            # guardamos los datos en el archivo txt
            if args.output is not None:
                txt = open(args.output, 'a')
                txt.write(datos)
                txt.close()
            print colored("+------------------------------------------+", "green", attrs=['bold'])
            print colored("\n [+] No se han encontrado mas datos\n", "red", attrs=['bold'])
        else:
            # si la respuesta no es 200 mostramos un error de conexion
            print colored("\n\n  Error en la conexión \n", "red", attrs=['bold'])
        conex.close()
    else:
        # si no se ha encontrado al menos una persona mostramos un mensaje de
        # error
        print colored(" [-] No se ha encontrado informacion\n", "red", attrs=['bold'])

# Si cancela la ejecucion, mostramos un mensaje de despedida
except KeyboardInterrupt:
    print colored("\n\n Ejecución cancelada, hasta la próxima!\n", "red", attrs=['bold'])
