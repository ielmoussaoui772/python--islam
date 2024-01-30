# Importamos los módulos necesarios
import csv
import subprocess
import sys

def leer_csv(csv_file):
    full_names = []
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            full_name = f"{first_name}{last_name}"  # Modificación: se elimina el espacio entre el primer nombre y el apellido
            full_names.append(full_name)
    
    return full_names

# Definimos una función para crear los usuarios del sistema con useradd
def crear_usuarios(csv_users):
    # Iteramos por cada usuario del csv
    for user in csv_users:
        # Creamos el comando para añadir el usuario con useradd
        command = f'useradd {user}'
        # Ejecutamos el comando con subprocess
        subprocess.run(command, shell=True)

# Definimos una función para borrar los usuarios del sistema que no están en el csv ni en la lista de usuarios protegidos
def borrar_usuarios(csv_users, protected_users):
    # Creamos una lista vacía para almacenar los nombres de los usuarios del sistema
    system_users = []
    # Creamos el comando para listar los usuarios del sistema
    command = 'cut -d: -f1 /etc/passwd'
    # Ejecutamos el comando con subprocess y capturamos la salida
    output = subprocess.run(command, shell=True, capture_output=True)
    # Convertimos la salida de bytes a cadena
    output = output.stdout.decode()
    # Dividimos la salida por saltos de línea
    output = output.split('\n')
    # Añadimos cada nombre de usuario a la lista de usuarios del sistema
    for user in output:
        system_users.append(user)
    # Iteramos por cada usuario del sistema
    for user in system_users:
        # Si el usuario no está en la lista de usuarios del csv ni en la lista de usuarios protegidos
        if user not in csv_users and user not in protected_users:
            # Creamos el comando para borrar el usuario con userdel
            command = f'userdel {user} > /dev/null 2&1'
            # Ejecutamos el comando con subprocess
            subprocess.run(command, shell=True)

# Definimos el nombre del archivo csv como un argumento
csv_file = sys.argv[1]

# Definimos una lista con los nombres de los usuarios que no se pueden borrar
protected_users = ['root', 'islam']

# Llamamos a la función leer_csv para obtener la lista de usuarios del csv
csv_users = leer_csv(csv_file)

# Llamamos a la función crear_usuarios para crear los usuarios del sistema
crear_usuarios(csv_users)

# Llamamos a la función borrar_usuarios para borrar los usuarios del sistema que no están en el csv ni en la lista de usuarios protegidos
borrar_usuarios(csv_users, protected_users)

