import sys
import logging
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Se requiere al menos un argumento para el nombre del archivo de registro.")
    else:
        logging.basicConfig(filename=sys.argv[1], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(str(os.getenv('USER')) + " Starting program")