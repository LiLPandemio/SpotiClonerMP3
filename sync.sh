#!/bin/bash

# Ejecutar main.py con python3 en segundo plano
python3 main.py &

# Guardar el PID del proceso de python3
python_pid=$!

# Esperar a que python3 main.py termine
wait $python_pid

# Ejecutar temp.sh con bash linea a linea para que si falla una cancion no se detenga
while IFS= read -r line; do
  eval "$line" || true
done < temp.sh

# Borrar temp.sh
rm temp.sh