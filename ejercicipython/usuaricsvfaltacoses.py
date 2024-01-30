#!/usr/bin/env python
import csv
import subprocess
import sys
import logging  

logging.basicConfig(filename="logprova.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)




def leer_csv(csv_file):
    full_names = []
    duplicates = [] # Crea una lista para guardar los nombres duplicados
    
    # Configura el archivo de registro y el formato de los mensajes
    logging.basicConfig(filename='duplicates.log', 
                        filemode='a', 
                        format='%(asctime)s - %(message)s', 
                        level=logging.INFO)
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            first_name = row['first_name'][0]
            last_name = row['last_name']
            full_name = f"{first_name}{last_name}"[:8] # Guarda solo los primeros 8 caracteres
            
            # Comprueba si el nombre ya está en la lista de nombres completos
            if full_name in full_names:
                # Si está repetido, lo añade a la lista de duplicados
                duplicates.append(full_name)
                # Y escribe un mensaje en el archivo de registro
                logging.info(f"Nombre duplicado: {full_name}")
            else:
                # Si no está repetido, lo añade a la lista de nombres completos
                full_names.append(full_name)
    
    return full_names




def crear_usuarios(csv_users):
    for user in csv_users:
        command = f'useradd {user}'
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
        logging.info(f"Usuario {user} creado")

def borrar_usuarios(csv_users, protected_users):
    system_users = []
    command = 'cut -d: -f1 /etc/passwd'
    output = subprocess.run(command, shell=True, capture_output=True)
    output = output.stdout.decode()
    output = output.split('\n')
    for user in output:
        system_users.append(user)
    for user in system_users:
        if user not in csv_users and user not in protected_users:
            command = f'userdel {user} > /dev/null 2&1'
            subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
            logging.info(f"Usuario {user} borrado")

csv_file = sys.argv[1]

protected_users = ['root', 'islam']

csv_users = leer_csv(csv_file)

crear_usuarios(csv_users)

borrar_usuarios(csv_users, protected_users) 
