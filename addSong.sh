#!/bin/bash

#
#   Descarga una cancion manualmente a la biblioteca
#

# Obtener el path
path=$(grep "output_dir" config.ini | cut -d "=" -f 2 | tr -d '\r')

# Guardar el path actual
pwd=$(pwd)

# Solicitar al usuario el título de la canción
read -p "Ingrese el título de la canción: " cancion

# Solicitar al usuario el nombre del artista
read -p "Ingrese el nombre del artista: " artista

# Imprimir las variables por separado
eval "cd $path"
eval "spotdl '$cancion - $artista'"
eval "cd $pwd"