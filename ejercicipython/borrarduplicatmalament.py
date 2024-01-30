# Importar las librerías necesarias
import os
import logging
import subprocess
import hashlib
import sys

# Función para crear el logger
def crear_logger():
    # Crear un logger para guardar el registro de las operaciones
    logger = logging.getLogger("remover")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("log.log")
    # Cambiar el formateador para incluir el nombre del archivo original, el archivo copia y el usuario
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - Archivo original: %(original)s, Archivo copia: %(message)s, Usuario: %(user)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# Función para calcular el hash de un archivo
def calcular_hash(file_path):
    # Calcular el hash del archivo usando SHA256
    hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Leer el archivo por bloques de 1024 bytes
        block = f.read(1024)
        while block:
            # Actualizar el hash con el bloque leído
            hash.update(block)
            # Leer el siguiente bloque
            block = f.read(1024)
    # Obtener el hash en formato hexadecimal
    hash = hash.hexdigest()
    return hash

# Función para comprobar si el hash está en el diccionario y realizar la acción correspondiente
def comprobar_hash(hash, file_path, hashes, logger):
    # Comprobar si el hash ya está en el diccionario
    if hash in hashes:
        # El archivo es una copia de otro archivo
        # Obtener el nombre del archivo original
        original = hashes[hash]
        # Borrar el archivo copia
        os.remove(file_path)
        # Obtener el nombre del usuario actual
        user = os.getenv("USERNAME")
        # Registrar la operación en el log
        # Pasar el nombre del archivo original y el usuario como argumentos extra
        logger.info(file_path, extra={"original": original, "user": user})
    else:
        # El archivo es único
        # Añadir el hash y el nombre del archivo al diccionario
        hashes[hash] = file_path
        # Registrar la operación en el log
        logger.info(f"Archivo único: {file_path}")

# Función principal que recorre el directorio y llama a las otras funciones
def main():
    # Crear el logger
    logger = crear_logger()
    # Crear un diccionario para almacenar los hashes y los nombres de los archivos
    hashes = {}
    # Obtener el directorio desde el argumento del programa
    directory = sys.argv[1]
    # Recorrer todos los archivos del directorio
    for file in os.listdir(directory):
        # Obtener el nombre completo del archivo
        file_path = os.path.join(directory, file)
        # Comprobar si el archivo es un archivo regular
        if os.path.isfile(file_path):
            # Calcular el hash del archivo
            hash = calcular_hash(file_path)
            # Comprobar el hash y realizar la acción correspondiente
            comprobar_hash(hash, file_path, hashes, logger)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
